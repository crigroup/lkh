#include "LKH.h"

int NNH()
{
    Node *From, *To, *Start, *NN;
    int Max = INT_MIN, Min, Visited = 0, D, i;

    for (i = 2; i <= DimensionSaved; i++)
        NodeSet[i].V = 0;
    Start = From = &NodeSet[1]; 
    while (++Visited < DimensionSaved) {
         From->V = 1;
         Min = INT_MAX;
         NN = 0;
         for (i = 2; i <= DimensionSaved; i++) {
             To = &NodeSet[i];
             if (!To->V && 
                 (D = ProblemType != ATSP ? Distance(From, To) : 
                  From->C[To->Id]) < Min) {
                 Min = D;
                 NN = To;
             }
         }
         From = NN;
         if (Min > Max)
             Max = Min;
    }
    D = ProblemType != ATSP ? Distance(From, Start) : From->C[Start->Id];
    if (D > Max)
        Max = D;
    return Max;
}
