#ifndef GUARD_LEGENDS_FIELD_REQUESTS_H
#define GUARD_LEGENDS_FIELD_REQUESTS_H

#include "constants/legends_field_requests.h"

extern u8 gLegendsFieldRequestMenuLabels[LEGENDS_REQUEST_PAGE_SIZE][48];
u16 LegendsFieldRequestActive(void);
bool32 LegendsFieldRequestUnlocked(u16 id);
u8 LegendsFieldRequestOwner(u16 id);
bool32 LegendsFieldRequestComplete(u16 id);
bool32 LegendsFieldRequestStepComplete(u16 id, u8 step);
u8 LegendsFieldRequestAccept(u16 id);
bool32 LegendsFieldRequestAbandon(void);
u8 LegendsFieldRequestSubmit(void);
void LegendsFieldRequestsObserve(void);
void LegendsFieldRequestsGetActive(void);
void LegendsFieldRequestsPrepareMenu(void);
void LegendsFieldRequestsDescribe(void);
void LegendsFieldRequestsAcceptSpecial(void);
void LegendsFieldRequestsReview(void);
void LegendsFieldRequestsSubmitSpecial(void);
void LegendsFieldRequestsAbandonSpecial(void);

void LegendsFieldRequestsBeginBirch(void);
void LegendsFieldRequestsBeginDevon(void);
void LegendsFieldRequestsGetPatron(void);
void LegendsFieldRequestsResearchNotes(void);
void LegendsFieldRequestsSelectGroup(void);
void LegendsFieldRequestsSelectRow(void);
void LegendsFieldRequestsCanReview(void);
void LegendsFieldRequestsGreeting(void);
#endif
