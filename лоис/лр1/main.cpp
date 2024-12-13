#include<iostream>
#include<cstdio>
#include<string>
#include<vector>
#include<algorithm>
#include<map>
#include<set>
#include<queue>

#include"parser.hpp"

using namespace std;

extern string s;
extern int pos;

struct Matrix{
    Rule rule;
    map<string, map<string, double>> matr;
};

double Implication(double a, double b){
    if(a <= b){
        return 1;
    } else {
        return 1 - a + b;
    }
}

Matrix createMatr(Fact& fact1, Fact& fact2, Rule& rule){
    Matrix matrix;
    matrix.rule = rule;

    for(int i = 0; i < fact1.fuzzySet.size(); i++){
        for(int j = 0; j < fact2.fuzzySet.size(); j++){
            matrix.matr[fact1.fuzzySet[i].first].insert({fact2.fuzzySet[j].first, Implication(fact1.fuzzySet[i].second, fact2.fuzzySet[j].second)});
        }
    }

    return matrix;
}

bool canConclusion(vector<pair<string,double>>& fuzzySet, Matrix& matrix){
    for(int i = 0; i < fuzzySet.size(); i++){
        if(matrix.matr.find(fuzzySet[i].first) == matrix.matr.end()){
            return false;
        }
    }

    return true;
}

double calcTNorma(double a, double b){
    return a * b;
}

vector<pair<string, double>> fuzzyConclusion(vector<pair<string, double>>& fuzzySet, Matrix& matrix){
    
    vector<pair<string, double>> newFuzzySet;

    {
        auto it1 = matrix.matr.begin()->second.begin();
        while(it1 != matrix.matr.begin()->second.end()){
            newFuzzySet.push_back({it1->first, 0});
            ++it1;
        }
    }

    for(int i = 0; i < newFuzzySet.size(); i++){
        double value = 0;
        for(int j = 0; j < fuzzySet.size(); j++){
            value = max(value, calcTNorma(fuzzySet[j].second, matrix.matr[fuzzySet[j].first][newFuzzySet[i].first]));
        }
        newFuzzySet[i].second = value;
    }

    return newFuzzySet;
}

int main(){
    string fileName; //cin >> fileName;
    fileName = "input.txt";

    freopen(fileName.c_str(), "r", stdin);

    vector<Fact> facts;
    vector<Rule> rules;

    bool flag = true;
    try{
        while(getline(cin, s)){
            if(s == ""){
               flag = false;
               continue;
            }
            pos = 0;

            if(flag){
                Fact fact = readFact();
                std::sort(fact.fuzzySet.begin(), fact.fuzzySet.end());
                facts.push_back(fact);
            } else {
                Rule rule = readRule();
                rules.push_back(rule);
            }
        }
    } catch(const char* b){
        cout << b;
        return 0;
    }

    vector<Matrix> v;
    for(int i = 0; i < rules.size(); i++){
        string name1 = rules[i].name1, name2 = rules[i].name2;
        Fact fact1, fact2;
        for(int j = 0; j < facts.size(); j++){
            if(facts[j].name == name1){
                fact1 = facts[j];
            }
            if(facts[j].name == name2){
                fact2 = facts[j];
            }
        }

        Matrix matrix = createMatr(fact1, fact2, rules[i]);
        v.push_back(matrix);
    }

    /*cout << "Facts\n";
    for(int i = 0; i < facts.size(); i++){
        cout << facts[i].name << '\n';
        for(int j = 0; j < facts[i].fuzzySet.size(); j++){
            cout << facts[i].fuzzySet[j].first << ' ' << facts[i].fuzzySet[j].second << '\n';
        }
        cout << "-----------------------------\n";
    }

    cout << "Rules\n";
    for(int i = 0; i < rules.size(); i++){
        cout << rules[i].name1 << ' ' << rules[i].name2 << '\n';
    }

    cout << "Matrix\n";

    for(int i = 0; i < v.size(); i++){
        cout << v[i].rule.name1 << "~>" << v[i].rule.name2 << '\n';
        for(auto it1 = v[i].matr.begin(); it1 != v[i].matr.end(); ++it1){
            cout << it1->first << ": ";
            for(auto it2 = it1->second.begin(); it2 != it1->second.end(); ++it2){
                cout << it2->first << ',' << it2->second << '|';
            }
            cout << '\n';
        } 
        cout << "------------------------------\n";
    }*/

    set<vector<pair<string, double>>> ans;
    queue<vector<pair<string, double>>> q;

    for(int i = 0; i < facts.size(); i++){
        q.push(facts[i].fuzzySet);
        ans.insert(facts[i].fuzzySet);
    }

    while(!q.empty()){
        auto fuzzySet = q.front();
        q.pop();

        for(int i = 0; i < v.size(); i++){
            if(!canConclusion(fuzzySet, v[i])){
               continue;
            }

            vector<pair<string,double>> newFuzzySet = fuzzyConclusion(fuzzySet, v[i]);
            sort(newFuzzySet.begin(), newFuzzySet.end());

            if(ans.find(newFuzzySet) == ans.end()){
                ans.insert(newFuzzySet);
                q.push(newFuzzySet);
            }
        }
    }

    for(int i = 0; i < facts.size(); i++){
        ans.erase(facts[i].fuzzySet);
    }

    //cout << ans.size();
    for(auto it = ans.begin(); it != ans.end(); ++it){
        cout << '{';
        for(int i = 0; i < it->size(); i++){
            cout << '<' << (*it)[i].first << ',' << (*it)[i].second << '>';
            if(i + 1 < it->size()){
                cout << ',';
            }
        }
        cout <<"}\n";
    }

    return 0;
}