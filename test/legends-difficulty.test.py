"""Exercise the production Casual option and move-choice gate with controlled turns."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]


def function(path, signature):
    text = (root / path).read_text()
    start = text.index(signature + "\n{")
    return text[start:text.index("\n}", start) + 2]


settings = root / "src/legends_settings.c"
config = next(line for line in settings.read_text().splitlines()
              if line.startswith("#define LEGENDS_CASUAL_DIFFICULTY_VALUE"))
sources = [
    function("src/legends_settings.c", "bool32 LegendsIsCasualDifficulty(void)"),
    function("src/legends_settings.c", "void LegendsSetCasualDifficulty(bool32 enabled)"),
    function("src/battle_ai_main.c", "static u8 ChooseCasualAlternative(enum BattlerId battler, struct ChosenAction chosen)"),
]
stubs = r"""
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
typedef uint8_t u8;
typedef uint32_t u32;
typedef int32_t s32;
typedef int bool32;
enum BattlerId { PLAYER, TRAINER, PARTNER, ALLIED_TRAINER, MAX_BATTLERS_COUNT };
enum Move { MOVE_NONE, CORRECT_ATTACK, RESISTED_ATTACK, STATUS_MOVE, BAD_TARGET };
enum {
    BATTLE_TYPE_TRAINER = 1, BATTLE_TYPE_LINK = 2, BATTLE_TYPE_RECORDED = 4, BATTLE_TYPE_PALACE = 8,
    MOVE_LIMITATIONS_ALL = 0xFFFF, RNG_LEGENDS_CASUAL_MISTAKE, RNG_LEGENDS_CASUAL_MOVE,
    MAX_MON_MOVES = 4,
};
struct ChosenAction { u8 moveIndex; enum BattlerId target; };
static struct { u8 legendsDifficulty; } save, *gSaveBlock2Ptr = &save;
static struct { enum Move moves[4]; } gBattleMons[4];
static struct { unsigned aiCalcInProgress, aiPredictionInProgress; } logic, *gAiLogicData = &logic;
static struct { s32 finalScore[4][4][4]; } battle, *gAiBattleData = &battle;
static u32 gBattleTypeFlags, chanceRoll, choiceRoll, chanceCalls, limitedMoves, deadBattlers;
static bool32 IsOnPlayerSide(enum BattlerId battler) { return battler % 2 == 0; }
static bool32 IsBattlerAlive(enum BattlerId battler) { return !(deadBattlers & (1u << battler)); }
static u32 CheckMoveLimitations(enum BattlerId battler, u32 prior, u32 scope)
{
    assert(battler == TRAINER && prior == 0 && scope == MOVE_LIMITATIONS_ALL);
    return limitedMoves;
}
static bool32 IsMoveUnusable(u32 slot, enum Move move, u32 limitations)
{
    return move == MOVE_NONE || (limitations & (1 << slot));
}
static bool32 ShouldConsiderMoveForBattler(enum BattlerId battler, enum BattlerId target, enum Move move)
{
    assert(battler == TRAINER && target == PLAYER);
    return move != BAD_TARGET;
}
static bool32 CanTargetBattler(enum BattlerId battler, enum BattlerId target, enum Move move)
{
    return ShouldConsiderMoveForBattler(battler, target, move) && IsBattlerAlive(target);
}
static bool32 RandomPercentage(u32 tag, u32 threshold)
{
    assert(tag == RNG_LEGENDS_CASUAL_MISTAKE && threshold == 15);
    chanceCalls++;
    return chanceRoll < threshold;
}
static u32 RandomUniform(u32 tag, u32 min, u32 max)
{
    assert(tag == RNG_LEGENDS_CASUAL_MOVE && min == 0);
    return choiceRoll % (max + 1);
}
"""
checks = r"""
int main(void)
{
    const struct ChosenAction best = {0, PLAYER};
    gBattleTypeFlags = BATTLE_TYPE_TRAINER;
    logic.aiCalcInProgress = true;
    gBattleMons[TRAINER].moves[0] = CORRECT_ATTACK;
    gBattleMons[TRAINER].moves[1] = RESISTED_ATTACK;
    gBattleMons[TRAINER].moves[2] = STATUS_MOVE;
    gBattleMons[TRAINER].moves[3] = BAD_TARGET;
    s32 *scores = battle.finalScore[TRAINER][PLAYER];
    scores[0] = 130; scores[1] = 75; scores[2] = 95; scores[3] = 70;

    assert(!LegendsIsCasualDifficulty());
    save.legendsDifficulty = 0xFF;
    assert(!LegendsIsCasualDifficulty());
    assert(ChooseCasualAlternative(TRAINER, best) == 0 && chanceCalls == 0);

    LegendsSetCasualDifficulty(true);
    assert(LegendsIsCasualDifficulty());
    unsigned alternatives = 0, weaker = 0, status = 0;
    for (chanceRoll = 0; chanceRoll < 100; chanceRoll++)
    {
        choiceRoll = chanceRoll;
        u8 chosen = ChooseCasualAlternative(TRAINER, best);
        alternatives += chosen != 0;
        weaker += chosen == 1;
        status += chosen == 2;
    }
    assert(alternatives == 15 && weaker > 0 && status > 0 && weaker + status == 15);

    chanceRoll = 0;
    limitedMoves = 1 << 1;
    assert(ChooseCasualAlternative(TRAINER, best) == 2);
    limitedMoves |= 1 << 2;
    chanceCalls = 0;
    assert(ChooseCasualAlternative(TRAINER, best) == 0 && chanceCalls == 0);
    limitedMoves = 0;
    scores[1] = scores[2] = scores[0];
    assert(ChooseCasualAlternative(TRAINER, best) == 0 && chanceCalls == 0);
    scores[1] = 75;

    for (int flag = BATTLE_TYPE_LINK; flag <= BATTLE_TYPE_PALACE; flag *= 2)
    {
        gBattleTypeFlags = BATTLE_TYPE_TRAINER | flag;
        assert(ChooseCasualAlternative(TRAINER, best) == 0);
    }
    gBattleTypeFlags = 0;
    assert(ChooseCasualAlternative(TRAINER, best) == 0);
    gBattleTypeFlags = BATTLE_TYPE_TRAINER;
    assert(ChooseCasualAlternative(PLAYER, best) == 0);
    assert(ChooseCasualAlternative(TRAINER, (struct ChosenAction){0, ALLIED_TRAINER}) == 0);
    deadBattlers = 1 << PLAYER;
    assert(ChooseCasualAlternative(TRAINER, best) == 0);
    deadBattlers = 0;
    logic.aiPredictionInProgress = true;
    assert(ChooseCasualAlternative(TRAINER, best) == 0);
    logic.aiPredictionInProgress = false;
    logic.aiCalcInProgress = false;
    assert(ChooseCasualAlternative(TRAINER, best) == 0 && chanceCalls == 0);
    LegendsSetCasualDifficulty(false);
    assert(save.legendsDifficulty == 0 && !LegendsIsCasualDifficulty());
    puts("Difficulty default, all 100 AI rolls, both alternatives, legality and exempt decisions passed.");
}
"""
with tempfile.TemporaryDirectory() as tmp:
    folder = Path(tmp)
    (folder / "difficulty.c").write_text("\n".join([stubs, config, *sources, checks]))
    subprocess.run(["cc", "-std=c99", "-Wall", "-Wextra", "-Werror", str(folder / "difficulty.c"),
                    "-o", str(folder / "check")], check=True)
    subprocess.run([str(folder / "check")], check=True)
