#ifndef FACT_H   // Если макрос FACT_H не определен
#define FACT_H   // Определяем макрос FACT_H

#include<string>
#include<vector>
#include<utility>

struct Fact {
    std::string name;
    std::vector<std::pair<std::string, double>> fuzzySet;
};

struct Rule{
    std::string name1, name2;
};

Fact readFact();

Rule readRule();

#endif // FACT_H
