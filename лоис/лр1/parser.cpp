
#include<vector>
#include<string>
#include"parser.hpp"

using namespace std;

int pos = 0;
char c;
double num;
string s, lex, name;

void nextChar(){
    if(pos < s.size()){
        c = s[pos];
        pos++;
    } else {
        c = '\n';
    }
}

void readName(){
    name = c;
    nextChar();

    while(('a' <= c && c <= 'z') || ('A' <= c && c <= 'Z')){
        name.push_back(c);
        nextChar();
    }

    while('0' <= c && c <= '9'){
        name.push_back(c);
        nextChar();
    }
}

void readNumber(){
    int pow = 10;
    num = c - '0';
    nextChar();

    if(num == 1){
        if(c == '.'){
            nextChar();
            if(c != '0'){
                throw "Parser error(Fact). Expected: 1.(0)";
            }
            while(c == '0'){
                nextChar();
            }
        }
    } else {
        if(c == '.'){
            nextChar();
            if(!('0' <= c && c <= '9')){
                throw "Parser error(Fact). Expected: 0.(1|2|3|4|5|6|7|8|9)";
            }

            while('0' <= c && c <= '9'){
                int d = c - '0';
                num += 1.0 * d / pow;
                pow *= 10;
                nextChar();
            }
        }
    }
}

void nextLex(){
    if(c == '('){
        lex = "(";
        nextChar();

    } else if (c == ')'){
        lex = ")";
        nextChar();

    } else if(('a' <= c && c <= 'z') || ('A' <= c && c <= 'Z')){
        lex = "name";
        readName();

    } else if(c == '0' || c == '1'){
        lex = "number";
        readNumber();

    } else if(c == ',') {
        lex = ",";
        nextChar();

    } else if(c == '='){
        lex = "=";
        nextChar();

    } else if(c == '<'){
        lex = "<";
        nextChar();

    } else if(c == '>'){
        lex = ">";
        nextChar();

    } else if(c == '{'){
        lex = "{";
        nextChar();

    } else if(c == '}'){
        lex = "}";
        nextChar();

    } else if(c == '~'){
        nextChar();
        if(c == '>'){
            nextChar();
            lex = "~>";
        } else {
            throw "Parser error(Fact). Expected: ~>";
        }

    } else if(c == '\n'){
        lex = "\n";
    } else {
        throw "Parser error(Fact). Unexpected lexem";
    }
}

pair<string, double> readPairOfFuzzy(){
    pair<string, double> pairOfFuzzy;
    if(lex != "<"){
        throw "Parser error(Fact). Expected: <";
    }

    nextLex();

    if(lex != "name"){
        throw "Parser error(Fact). Expected: element name";
    }

    pairOfFuzzy.first = name;

    nextLex();
    if(lex != ","){
        throw "Parser error(Fact). Expected: ,";
    }

    nextLex();
    if(lex != "number"){
        throw "Parser error(Fact). Expected: number";
    }

    pairOfFuzzy.second = num;
    
    nextLex();
    if(lex != ">"){
        throw "Parser error(Fact). Expected: >";
    }

    nextLex();

    return pairOfFuzzy;
}

vector<pair<string, double>> readFuzzySet(){
    if(lex != "{"){
        throw "Parser error(Fact). Expected: {";
    }

    vector<pair<string, double>> fuzzy_set;
    nextLex();
   
    if(lex != "<"){
        throw "Parser error(Fact). Expected: <";
    }

    pair<string, double> pairOfFuzzy = readPairOfFuzzy();
    fuzzy_set.push_back(pairOfFuzzy);

    while(lex == ","){
        nextLex();
        pair<string, double> pairOfFuzzy = readPairOfFuzzy();
        fuzzy_set.push_back(pairOfFuzzy);
    }

    if(lex != "}"){
        throw "Parser error(Fact). Expected: }";
    }

    nextLex();

    return fuzzy_set;
}

Fact readFact(){
    Fact fact;

    nextChar();
    nextLex();

    if(lex != "name"){
        throw "Parser error(Fact). Expected: name of the fuzzy predicate";
    }

    fact.name = name;

    nextLex();
    if(lex != "="){
        throw "Parser error(Fact). Expected: =";
    }

    nextLex();
    auto fuzzySet = readFuzzySet();

    fact.fuzzySet = fuzzySet;

    if(lex != "\n"){
        throw "Parser error(Fact). Expected: end of line";
    }

    return fact;
};

Rule readRule(){
    Rule rule;

    nextChar();
    nextLex();

    if(lex != "name"){
        throw "Parser error(Rule). Expected: name of the fuzzy predicate";
    }

    rule.name1 = name;

    nextLex();
    if(lex != "~>"){
        throw "Parser error(Rule). Expected: ~>";
    }

    nextLex();
    if(lex != "name"){
        throw "Parser error(Rule). Expected: name of the fuzzy predicate";
    }

    rule.name2 = name;

    nextLex();
    if(lex != "\n"){
        throw "Parser error(Rule). Expected: end of line";
    }

    return rule;
}