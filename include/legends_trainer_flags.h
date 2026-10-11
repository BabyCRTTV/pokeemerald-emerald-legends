#ifndef GUARD_LEGENDS_TRAINER_FLAGS_H
#define GUARD_LEGENDS_TRAINER_FLAGS_H

// Trainer table capacity is independent of saved native trainer-flag capacity.
// Both teams of a visiting Gym resolve to its existing permanent victory bit.
static inline u16 LegendsTrainerFlag(u16 trainerId)
{
#if !IS_FRLG
    switch (trainerId)
    {
    case TRAINER_LEGENDS_KANTO_ERIKA_STANDARD:
    case TRAINER_LEGENDS_KANTO_ERIKA_CHAMPION:
        return FLAG_LEGENDS_KANTO_ERIKA_WON;
    case TRAINER_LEGENDS_KANTO_SABRINA_STANDARD:
    case TRAINER_LEGENDS_KANTO_SABRINA_CHAMPION:
        return FLAG_LEGENDS_KANTO_SABRINA_WON;
    }
#endif
    if (trainerId < MAX_TRAINERS_COUNT)
        return TRAINER_FLAGS_START + trainerId;
    return 0; // Partners/special opponents have no ordinary trainer victory bit.
}
#endif
