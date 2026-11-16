#include "global.h"
#include "event_data.h"
#include "item.h"
#include "main.h"
#include "item_menu.h"
#include "legends_meals.h"
#include "overworld.h"
#include "string_util.h"
#include "text.h"
#include "constants/items.h"

#define MEAL_SAVE_SIGNATURE 0x314C414D // MAL1
#define RECIPE_INGREDIENTS 4

struct MealRecipe
{
    enum Item meal;
    enum Item supplies[RECIPE_INGREDIENTS];
    enum LegendsMealEffect effect;
    u8 amount;
    const u8 *effectText;
    bool8 isDrink;
};

// Recipe indices are referenced by the cooking scripts. Each supply costs one unit.
static const struct MealRecipe sRecipes[] =
{
    {ITEM_BUTTER_OMELET, {ITEM_BUTTER, ITEM_EGG, ITEM_SALT, ITEM_PEPPER},
        MEAL_EFFECT_CATCH, 5, COMPOUND_STRING("Catch odds +5%"), FALSE},
    {ITEM_PANCAKES, {ITEM_FLOUR, ITEM_EGG, ITEM_COOKING_WATER, ITEM_BUTTER},
        MEAL_EFFECT_EXPERIENCE, 10, COMPOUND_STRING("Battle Exp. +10%"), FALSE},
    {ITEM_FLATBREAD, {ITEM_FLOUR, ITEM_COOKING_WATER, ITEM_SALT, ITEM_BUTTER},
        MEAL_EFFECT_PRIZE, 10, COMPOUND_STRING("Trainer prize money +10%"), FALSE},
    {ITEM_EGG_DROP_SOUP, {ITEM_EGG, ITEM_COOKING_WATER, ITEM_SALT, ITEM_PEPPER},
        MEAL_EFFECT_ENCOUNTER, 15, COMPOUND_STRING("Wild encounter rate -15%"), FALSE},
    {ITEM_CRACKERS, {ITEM_FLOUR, ITEM_COOKING_WATER, ITEM_SALT, ITEM_PEPPER},
        MEAL_EFFECT_FRIENDSHIP, 1, COMPOUND_STRING("Walk friendship +1"), FALSE},
    {ITEM_HOT_COCOA, {ITEM_COOKING_MILK, ITEM_SUGAR, ITEM_COCOA_POWDER},
        MEAL_EFFECT_FRIENDSHIP, 2, COMPOUND_STRING("Walk friendship +2"), TRUE},
    {ITEM_EGG_CUSTARD, {ITEM_EGG, ITEM_COOKING_MILK, ITEM_SUGAR},
        MEAL_EFFECT_EXPERIENCE, 15, COMPOUND_STRING("Battle Exp. +15%"), FALSE},
    {ITEM_MILK_COFFEE, {ITEM_COFFEE_GROUNDS, ITEM_COOKING_WATER, ITEM_COOKING_MILK},
        MEAL_EFFECT_EXPERIENCE, 10, COMPOUND_STRING("Battle Exp. +10%"), TRUE},
    {ITEM_SWEET_TEA, {ITEM_TEA_LEAVES, ITEM_COOKING_WATER, ITEM_SUGAR},
        MEAL_EFFECT_CATCH, 5, COMPOUND_STRING("Catch odds +5%"), TRUE},
    {ITEM_MATCHA_LATTE, {ITEM_MATCHA_POWDER, ITEM_COOKING_WATER, ITEM_COOKING_MILK},
        MEAL_EFFECT_FRIENDSHIP, 2, COMPOUND_STRING("Walk friendship +2"), TRUE},
    {ITEM_BREWED_OOLONG, {ITEM_OOLONG_TEA, ITEM_COOKING_WATER},
        MEAL_EFFECT_ENCOUNTER, 10, COMPOUND_STRING("Wild encounter rate -10%"), TRUE},
    {ITEM_BREWED_BLACK_TEA, {ITEM_BLACK_TEA, ITEM_COOKING_WATER},
        MEAL_EFFECT_PRIZE, 10, COMPOUND_STRING("Trainer prize money +10%"), TRUE},
    {ITEM_BLACK_COFFEE, {ITEM_COOKING_COFFEE, ITEM_COOKING_WATER},
        MEAL_EFFECT_EXPERIENCE, 10, COMPOUND_STRING("Battle Exp. +10%"), TRUE},
    {ITEM_HOJICHA_LATTE, {ITEM_HOJICHA_POWDER, ITEM_COOKING_WATER, ITEM_COOKING_MILK},
        MEAL_EFFECT_FRIENDSHIP, 2, COMPOUND_STRING("Walk friendship +2"), TRUE},
    {ITEM_HOJICHA_TEA, {ITEM_HOJICHA_LEAVES, ITEM_COOKING_WATER},
        MEAL_EFFECT_FRIENDSHIP, 1, COMPOUND_STRING("Walk friendship +1"), TRUE},
    {ITEM_TOMATO_FLATBREAD, {ITEM_FLOUR, ITEM_COOKING_WATER, ITEM_COOKING_TOMATO, ITEM_COOKING_CHEESE},
        MEAL_EFFECT_PRIZE, 15, COMPOUND_STRING("Trainer prize money +15%"), FALSE},
    {ITEM_BUTTERED_POTATOES, {ITEM_COOKING_POTATO, ITEM_BUTTER, ITEM_SALT},
        MEAL_EFFECT_ENCOUNTER, 10, COMPOUND_STRING("Wild encounter rate -10%"), FALSE},
    {ITEM_CARROT_SOUP, {ITEM_COOKING_CARROT, ITEM_COOKING_ONION, ITEM_COOKING_WATER, ITEM_SALT},
        MEAL_EFFECT_ENCOUNTER, 15, COMPOUND_STRING("Wild encounter rate -15%"), FALSE},
    {ITEM_ONION_TART, {ITEM_COOKING_ONION, ITEM_COOKING_CHEESE, ITEM_FLOUR, ITEM_BUTTER},
        MEAL_EFFECT_PRIZE, 15, COMPOUND_STRING("Trainer prize money +15%"), FALSE},
    {ITEM_APPLE_PANCAKES, {ITEM_COOKING_APPLE, ITEM_FLOUR, ITEM_EGG, ITEM_BUTTER},
        MEAL_EFFECT_EXPERIENCE, 15, COMPOUND_STRING("Battle Exp. +15%"), FALSE},
    {ITEM_POTATO_HASH, {ITEM_COOKING_POTATO, ITEM_COOKING_ONION, ITEM_BUTTER, ITEM_PEPPER},
        MEAL_EFFECT_CATCH, 5, COMPOUND_STRING("Catch odds +5%"), FALSE},
    {ITEM_EGGNOG, {ITEM_EGG, ITEM_COOKING_MILK, ITEM_SUGAR, ITEM_CINNAMON},
        MEAL_EFFECT_FRIENDSHIP, 2, COMPOUND_STRING("Walk friendship +2"), TRUE},
    {ITEM_SPICED_CIDER, {ITEM_COOKING_APPLE, ITEM_COOKING_WATER, ITEM_CINNAMON, ITEM_SUGAR},
        MEAL_EFFECT_PRIZE, 10, COMPOUND_STRING("Trainer prize money +10%"), TRUE},
    {ITEM_ICED_CINNAMON_COFFEE, {ITEM_COFFEE_GROUNDS, ITEM_COOKING_WATER, ITEM_CINNAMON, ITEM_ICE_CUBES},
        MEAL_EFFECT_EXPERIENCE, 10, COMPOUND_STRING("Battle Exp. +10%"), TRUE},
    {ITEM_GARLIC_RICE_PILAF, {ITEM_COOKING_RICE, ITEM_COOKING_GARLIC, ITEM_BUTTER, ITEM_COOKING_ONION},
        MEAL_EFFECT_ENCOUNTER, 15, COMPOUND_STRING("Wild encounter rate -15%"), FALSE},
    {ITEM_TOMATO_RICE, {ITEM_COOKING_RICE, ITEM_COOKING_TOMATO, ITEM_COOKING_ONION, ITEM_SALT},
        MEAL_EFFECT_PRIZE, 10, COMPOUND_STRING("Trainer prize money +10%"), FALSE},
    {ITEM_LEMON_SHORTBREAD, {ITEM_COOKING_LEMON, ITEM_FLOUR, ITEM_BUTTER, ITEM_SUGAR},
        MEAL_EFFECT_CATCH, 5, COMPOUND_STRING("Catch odds +5%"), FALSE},
    {ITEM_VANILLA_PUDDING, {ITEM_COOKING_RICE, ITEM_COOKING_MILK, ITEM_COOKING_VANILLA, ITEM_SUGAR},
        MEAL_EFFECT_FRIENDSHIP, 2, COMPOUND_STRING("Walk friendship +2"), FALSE},
    {ITEM_ICED_LEMONADE, {ITEM_COOKING_LEMON, ITEM_COOKING_WATER, ITEM_SUGAR, ITEM_ICE_CUBES},
        MEAL_EFFECT_FRIENDSHIP, 1, COMPOUND_STRING("Walk friendship +1"), TRUE},
    {ITEM_VANILLA_LATTE, {ITEM_COFFEE_GROUNDS, ITEM_COOKING_WATER, ITEM_COOKING_MILK, ITEM_COOKING_VANILLA},
        MEAL_EFFECT_EXPERIENCE, 15, COMPOUND_STRING("Battle Exp. +15%"), TRUE},
};

static const struct MealRecipe *GetRecipeByItem(enum Item item)
{
    for (u32 i = 0; i < ARRAY_COUNT(sRecipes); i++)
        if (sRecipes[i].meal == item)
            return &sRecipes[i];
    return NULL;
}

static bool32 MealSaveValid(void)
{
    return gSaveBlock3Ptr != NULL && gSaveBlock3Ptr->meals.signature == MEAL_SAVE_SIGNATURE;
}

static bool32 BuffActive(const struct LegendsMealBuff *buff)
{
    return buff->framesLeft != 0 && buff->framesLeft <= LEGENDS_MEAL_DURATION
        && GetRecipeByItem(buff->item) != NULL;
}

void LegendsMealTick(void)
{
    if (!MealSaveValid())
        return;
    for (u32 i = 0; i < LEGENDS_MEAL_SLOTS; i++)
    {
        struct LegendsMealBuff *buff = &gSaveBlock3Ptr->meals.buffs[i];
        if (buff->framesLeft != 0 && --buff->framesLeft == 0)
            buff->item = ITEM_NONE;
    }
}

u8 LegendsMealBonus(enum LegendsMealEffect effect)
{
    u8 total = 0;
    if (!MealSaveValid())
        return 0;
    for (u32 i = 0; i < LEGENDS_MEAL_SLOTS; i++)
    {
        const struct LegendsMealBuff *buff = &gSaveBlock3Ptr->meals.buffs[i];
        if (BuffActive(buff))
        {
            const struct MealRecipe *recipe = GetRecipeByItem(buff->item);
            if (recipe->effect == effect)
                total += recipe->amount;
        }
    }
    return total;
}

bool32 LegendsMealReadSlot(u32 slot, enum Item *item, u32 *seconds)
{
    if (slot >= LEGENDS_MEAL_SLOTS || !MealSaveValid())
        return FALSE;
    const struct LegendsMealBuff *buff = &gSaveBlock3Ptr->meals.buffs[slot];
    if (!BuffActive(buff))
        return FALSE;
    *item = buff->item;
    *seconds = (buff->framesLeft + LEGENDS_MEAL_FRAMES_PER_SECOND - 1) / LEGENDS_MEAL_FRAMES_PER_SECOND;
    return TRUE;
}

const u8 *LegendsMealEffectText(enum Item item)
{
    const struct MealRecipe *recipe = GetRecipeByItem(item);
    return recipe != NULL ? recipe->effectText : COMPOUND_STRING("");
}

bool32 LegendsMealIsDrink(enum Item item)
{
    const struct MealRecipe *recipe = GetRecipeByItem(item);
    return recipe != NULL && recipe->isDrink;
}

enum LegendsCookResult LegendsCookMeal(u32 recipeIndex)
{
    if (recipeIndex >= ARRAY_COUNT(sRecipes))
        return LEGENDS_COOK_MISSING;

    const struct MealRecipe *recipe = &sRecipes[recipeIndex];
    struct BagPocket *supplies = &gBagPockets[POCKET_ITEMS];
    struct BagPocket *food = &gBagPockets[POCKET_FOOD];
    u16 supplySlots[RECIPE_INGREDIENTS];
    u16 supplyQuantities[RECIPE_INGREDIENTS];
    bool32 freesStack = FALSE;
    u16 targetSlot = food->capacity;
    u16 targetQuantity = 0;
    u32 ingredientCount;

    // Preflight every ingredient and the output slot before mutating anything.
    for (ingredientCount = 0; ingredientCount < RECIPE_INGREDIENTS; ingredientCount++)
    {
        enum Item ingredient = recipe->supplies[ingredientCount];
        if (ingredient == ITEM_NONE)
            break;
        u32 slot;
        for (slot = 0; slot < supplies->capacity; slot++)
        {
            struct ItemSlot entry = BagPocket_GetSlotData(supplies, slot);
            if (entry.itemId == ingredient && entry.quantity > 0)
            {
                supplySlots[ingredientCount] = slot;
                supplyQuantities[ingredientCount] = entry.quantity;
                freesStack |= entry.quantity == 1;
                break;
            }
        }
        if (slot == supplies->capacity)
            return LEGENDS_COOK_MISSING;
    }

    for (u32 slot = 0; slot < food->capacity; slot++)
    {
        struct ItemSlot entry = BagPocket_GetSlotData(food, slot);
        if (entry.itemId == ITEM_NONE ||
            (entry.itemId == recipe->meal && entry.quantity < MAX_BAG_ITEM_CAPACITY))
        {
            targetSlot = slot;
            targetQuantity = entry.itemId == ITEM_NONE ? 0 : entry.quantity;
            break;
        }
    }
    if (targetSlot == food->capacity && !freesStack)
        return LEGENDS_COOK_BAG_FULL;

    // Slot updates trim trailing empty slots only. Compact after all indexed
    // deductions, then insert the meal using the refreshed shared-pool capacity.
    for (u32 i = 0; i < ingredientCount; i++)
        BagPocket_SetSlotData(supplies, supplySlots[i],
            (struct ItemSlot){recipe->supplies[i], supplyQuantities[i] - 1});
    CompactItemsInBagPocket(POCKET_ITEMS);
    BagPocket_SetSlotData(food, targetSlot, (struct ItemSlot){recipe->meal, targetQuantity + 1});
    GetSetItemObtained(recipe->meal, FLAG_SET_ITEM_OBTAINED);
    return LEGENDS_COOK_SUCCESS;
}

enum LegendsEatResult LegendsEatMeal(enum Item item)
{
    if (GetRecipeByItem(item) == NULL || !CheckBagHasItem(item, 1))
        return LEGENDS_EAT_UNAVAILABLE;

    struct LegendsMealSave *save = &gSaveBlock3Ptr->meals;
    if (!MealSaveValid())
    {
        memset(save, 0, sizeof(*save));
        save->signature = MEAL_SAVE_SIGNATURE;
    }
    for (u32 i = 0; i < LEGENDS_MEAL_SLOTS; i++)
    {
        if (!BuffActive(&save->buffs[i]))
        {
            if (!RemoveBagItem(item, 1))
                return LEGENDS_EAT_UNAVAILABLE;
            save->buffs[i] = (struct LegendsMealBuff){item, LEGENDS_MEAL_DURATION};
            return LEGENDS_EAT_SUCCESS;
        }
    }
    return LEGENDS_EAT_FULL;
}

void Script_LegendsCookMeal(void)
{
    gSpecialVar_Result = LegendsCookMeal(gSpecialVar_0x8004);
    if (gSpecialVar_Result == LEGENDS_COOK_SUCCESS)
    {
        const struct MealRecipe *recipe = &sRecipes[gSpecialVar_0x8004];
        gSpecialVar_0x8006 = recipe->isDrink;
        CopyItemName(recipe->meal, gStringVar1);
    }
}

static void Task_AcknowledgeMeal(u8 taskId)
{
    if (JOY_NEW(A_BUTTON | B_BUTTON))
        CloseItemMessage(taskId);
}

void ItemUseOutOfBattle_LegendsMeal(u8 taskId)
{
    const u8 *message;
    bool32 isDrink = LegendsMealIsDrink(gSpecialVar_ItemId);
    switch (LegendsEatMeal(gSpecialVar_ItemId))
    {
    case LEGENDS_EAT_SUCCESS:
        CopyItemName(gSpecialVar_ItemId, gStringVar1);
        StringExpandPlaceholders(gStringVar4, isDrink
            ? COMPOUND_STRING("You drank the {STR_VAR_1}!\nIts buff lasts 10 minutes.")
            : COMPOUND_STRING("You ate the {STR_VAR_1}!\nIts buff lasts 10 minutes."));
        message = gStringVar4;
        break;
    case LEGENDS_EAT_FULL:
        message = isDrink
            ? COMPOUND_STRING("You're too full to drink more!\p"
                "Wait a little while before\ndrinking again.")
            : COMPOUND_STRING("You're too full to eat more!\p"
                "Wait a little while before\neating again.");
        break;
    default:
        message = isDrink ? COMPOUND_STRING("You couldn't drink that.")
            : COMPOUND_STRING("You couldn't eat that meal.");
        break;
    }
    DisplayItemMessage(taskId, FONT_NORMAL, message, Task_AcknowledgeMeal);
}
