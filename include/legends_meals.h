#ifndef GUARD_LEGENDS_MEALS_H
#define GUARD_LEGENDS_MEALS_H

#define LEGENDS_MEAL_FRAMES_PER_SECOND 60
#define LEGENDS_MEAL_MINUTES 10
#define LEGENDS_MEAL_DURATION (LEGENDS_MEAL_MINUTES * 60 * LEGENDS_MEAL_FRAMES_PER_SECOND)
#define LEGENDS_RECIPE_INGREDIENTS 4
#define LEGENDS_COOKING_VISIBLE_ROWS 8

struct ScriptContext;

enum LegendsMealEffect
{
    MEAL_EFFECT_CATCH,
    MEAL_EFFECT_EXPERIENCE,
    MEAL_EFFECT_PRIZE,
    MEAL_EFFECT_ENCOUNTER,
    MEAL_EFFECT_FRIENDSHIP,
};

enum LegendsCookResult
{
    LEGENDS_COOK_MISSING,
    LEGENDS_COOK_SUCCESS,
    LEGENDS_COOK_BAG_FULL,
};

enum LegendsEatResult
{
    LEGENDS_EAT_UNAVAILABLE,
    LEGENDS_EAT_SUCCESS,
    LEGENDS_EAT_FULL,
};

void LegendsMealTick(void);
u8 LegendsMealBonus(enum LegendsMealEffect effect);
bool32 LegendsMealReadSlot(u32 slot, enum Item *item, u32 *seconds);
const u8 *LegendsMealEffectText(enum Item item);
bool32 LegendsMealIsDrink(enum Item item);
enum LegendsCookResult LegendsCookMeal(u32 recipeIndex);
enum LegendsEatResult LegendsEatMeal(enum Item item);
const enum Item *LegendsMealRecipePreview(u32 recipeIndex, enum Item *meal);
void Script_LegendsChooseRecipe(struct ScriptContext *ctx);
void Script_LegendsCookMeal(void);
void ItemUseOutOfBattle_LegendsMeal(u8 taskId);

#endif
