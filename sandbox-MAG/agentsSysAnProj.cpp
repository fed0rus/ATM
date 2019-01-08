#include <bits/stdc++.h>
#include <windows.h>

/// SURVAVIUM

using namespace std;

// Reinforcement learning - Обучение с подкреплением



const int n_of_b = 4;        // Number of bots, which will be crossover

const int number_of_iterations = 100000;

const int mod = 4;          // Number of Bot's commands

const int max_health = 30;   // Bot's max health

const int Fruit_Power = 15 + 1;    // Fruit add to health "Fruit_Power" points

const int Poison_Power = 7 - 1;    // Poison take "Poison_Power" points by health

const int Bots_Number = 8;         // Number of Bots

const int Probability = mod * mod * mod * mod * 2;          // REALPROBABILITY = 1 / Probability

const int width = 18;
const int height = 18;


int area[height][width];

/**** Legend ****
 *  -1                   - Wall
 *  0                    - Empty place
 *  [1; max_health]      - Bot (Bot's health)
 *  -2                   - Fruit
 *  -3                   - Poison
 */






void printm() {
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            if (area[i][j] < 10 && area[i][j] >= 0) cout << "0" << area[i][j] << "  ";
            else cout << area[i][j] << "  ";
        }
        cout << endl;
    }
}

double ran(double mi, double ma) {
    double q;
    q = rand()/(double)(RAND_MAX + 1);
    return q * (ma - mi) + mi;
}


struct Bot {
    int x;
    int y;
    int health;
    int counter = 0;

    //pair<int, int> killed;

    /**** Commands ****
     *  0 - 3 - step:
     *        0 - up;
     *        1 - right;
     *        2 - down;
     *        3 - left.
     */

    int commands[2 * mod * mod * mod * mod];
    int steps[4][2] = {{0, -1}, {-1, 0}, {0, 1}, {1, 0}};




    void do_comm()
    {
        counter = 0;
        if (area[x + steps[0][0]][y + steps[0][1]] > 0) counter += 1;
        else counter += abs(area[x + steps[0][0]][y + steps[0][1]]);
        if (area[x + steps[1][0]][y + steps[1][1]] > 0) counter += 4;
        else counter += abs(area[x + steps[1][0]][y + steps[1][1]]) * 4;
        if (area[x + steps[2][0]][y + steps[2][1]] > 0) counter += 4 * 4;
        else counter += abs(area[x + steps[2][0]][y + steps[2][1]]) * 4 * 4;
        if (area[x + steps[3][0]][y + steps[3][1]] > 0) counter += 4 * 4 * 4;
        else counter += abs(area[x + steps[3][0]][y + steps[3][1]]) * 4 * 4 * 4;
        counter *= 2;
        int z = commands[counter];
        commands[counter] = commands[counter + 1];
        commands[counter + 1] = z;



        if (commands[counter] >= 0 && commands[counter] < 4) {
            if (area[x + steps[commands[counter]][0]][y + steps[commands[counter]][1]] == 0) {          // Check vacant place; empty place
                area[x][y] = 0;
                x += steps[commands[counter]][0];
                y += steps[commands[counter]][1];
            }
            else if (area[x + steps[commands[counter]][0]][y + steps[commands[counter]][1]] == -2) {    // Fruit
                area[x][y] = 0;
                x += steps[commands[counter]][0];
                y += steps[commands[counter]][1];
                health += Fruit_Power;
                if (health > max_health) health = max_health;
            }
            else if (area[x + steps[commands[counter]][0]][y + steps[commands[counter]][1]] == -3) {    // Poison
                area[x][y] = 0;
                x += steps[commands[counter]][0];
                y += steps[commands[counter]][1];
                health -= Poison_Power;
            }

            /*
            else if (area[x + steps[commands[counter]][0]][y + steps[commands[counter]][1]] > 0) {      // Another bot will be feeling like a wall now




                int attack_prob = ran(0, 1.999999);        //50% - attack = own_health / 4; 50% - attack = own_health / 2
                int damage_prob = ran(0, 1.999999);        //50% - damage = foreign_health / 4; 50% - damage = foreign_health / 2
                int attack;
                int damage;
                int foreign_health = area[x + steps[commands[counter]][0]][y + steps[commands[counter]][1]];
                if (attack_prob == 0) attack = health / 4;
                else attack = health / 2;
                if (damage_prob == 0) damage = foreign_health / 4;
                else damage = foreign_health / 2;
                if (foreign_health > attack) {
                    foreign_health -= attack;
                    health -= damage;
                }
                else {
                    area[x + steps[commands[counter]][0]][y + steps[commands[counter]][1]] = health;
                    killed = {x + steps[commands[counter]][0], y + steps[commands[counter]][1]};
                    ///ДОДЕЛАТЬ!!!
                }


            }
            */
            health--;           // if bot try to go in wall or in another bot it will do nothing
            if (health < 0) health = 0;
            area[x][y] = health;
            counter = (counter + 1) % mod;
        }
    }

};

int counted(vector<int> GG) {
    int resultat = 0;
    for (auto e : GG) {
        if (e == 0) resultat = 1;
    }
    return resultat;
}

void Selection(vector<Bot> &Bots, vector<int> &Active_Bots) {
    for (int i = 0; i < Bots.size(); i++) {
        if (Active_Bots[i] > 1 && Active_Bots[i] <= 5) {
            Active_Bots.erase(Active_Bots.begin() + i);
            Bots.erase(Bots.begin() + i);
            i--;
        }
    }
}

void Uniform_Crossover(vector<Bot> &Bots) {
    for (int i = 0; i < Bots_Number - n_of_b; i++) {
        int n1 = ran(0, n_of_b - 0.0001);
        int n2;
        do {
            n2 = ran(0, n_of_b - 0.0001);
        } while (n2 == n1);

        Bot New_Bot;
        for (int j = 0; j < 2 * mod * mod * mod * mod; j++) {
            int uk = ran(0, 1.99999);
            if (uk == 0) {
                New_Bot.commands[j] = Bots[n1].commands[j];
            }
            else New_Bot.commands[j] = Bots[n2].commands[j];
        }
        Bots.push_back(New_Bot);
    }
}

void Best_Crossover(vector<Bot> &Bots, vector<int> Active_Bots) {
    for (int i = 0; i < Bots_Number - n_of_b; i++) {
        int n1 = ran(0, n_of_b - 0.0001);
        int n2;
        do {
            n2 = ran(0, n_of_b - 0.0001);
        } while (n2 == n1);

        Bot New_Bot;
        if (Active_Bots[n1] < Active_Bots[n2]) {
            n1 = n2;
        }
        for (int j = 0; j < 2 * mod * mod * mod * mod; j++) {
            New_Bot.commands[j] = Bots[n1].commands[j];
        }
        Bots.push_back(New_Bot);
    }
}

void Other_Crossover(vector<Bot> &Bots) {
    for (int i = 0; i < Bots_Number - n_of_b; i++) {
        int n1 = ran(0, n_of_b - 0.0001);
        int n2;
        do {
            n2 = ran(0, n_of_b - 0.0001);
        } while (n2 == n1);
        Bot New_Bot;
        int razd = ran(0, 2 * mod * mod * mod * mod - 0.0001);
        for (int j = 0; j < razd; j++) {
            New_Bot.commands[j] = Bots[n1].commands[j];
        }
        for (int j = razd; j < 2 * mod * mod * mod * mod; j++) {
            New_Bot.commands[j] = Bots[n2].commands[j];
        }
        Bots.push_back(New_Bot);
    }
}



void Mutation(vector<Bot> &Bots) {
    for (int i = 0; i < Bots.size(); i++) {
        for (int j = 0; j < 2 * mod * mod * mod * mod; j++) {
            int uk = ran(0, Probability - 0.00001);
            if (uk == 0) {
                int now_c = Bots[i].commands[j];
                int new_c;
                do {
                    new_c = ran(0, 4 - 0.00001);
                } while (now_c == new_c);
                Bots[i].commands[j] = new_c;
            }
        }
    }
}





int main()
{
    srand((unsigned)time(NULL));
    int dich = ran(0, 1);




    vector<Bot> Bots(Bots_Number);
    for (int i = 0; i < Bots_Number; i++) {
        for (int j = 0; j < mod * mod * mod * mod * 2; j++) {
            Bots[i].commands[j] = (int) ran(0, 4 - 0.0001);
        }
    }



    int result = 0, iter = 0;

    for (int S = 0; S < number_of_iterations; S++) {

        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                if (i == 0 || j == 0 || i == height - 1 || j == width - 1) area[i][j] = -1;
                else area[i][j] = 0;
            }
        }

        vector<int> Active_Bots(Bots_Number, 0);
        //map<pair<int, int>, int> Bots_places;
        int Curr_Bot = 0;


        for (int i = 0; i < Bots.size(); i++) {
            int temp_x = ran(1, height - 1.00001);
            int temp_y = ran(1, width - 1.00001);
            while (area[temp_x][temp_y] != 0) {
                temp_x = ran(1, height - 1.00001);
                temp_y = ran(1, width - 1.00001);
            }
            //Bots[i].killed = {-1, -1};
            Bots[i].x = temp_x;
            Bots[i].y = temp_y;
            //Bots_places.[{temp_x, temp_y}] = i;
            Bots[i].health = max_health;
            area[Bots[i].x][Bots[i].y] = max_health;
        }

        for (int fruits = 0; fruits < 6; fruits++) {
            int f_x, f_y;
            do {
                f_x = ran(1, height - 1.00001);
                f_y = ran(1, width - 1.00001);
            } while (area[f_x][f_y] != 0);
            area[f_x][f_y] = -2;
        }

        for (int poisons = 0; poisons < 6; poisons++) {
            int p_x, p_y;
            do {
                p_x = ran(1, height - 1.00001);
                p_y = ran(1, width - 1.00001);
            } while (area[p_x][p_y] != 0);
            area[p_x][p_y] = -3;
        }



        int numb_of_iteration = 0;
        while (counted(Active_Bots)) {
            numb_of_iteration++;
            if (numb_of_iteration % 2 == 0) {
                int f_x, f_y;
                do {
                    f_x = ran(1, height - 1.00001);
                    f_y = ran(1, width - 1.00001);
                } while (area[f_x][f_y] != 0);
                area[f_x][f_y] = -2;
            }
            if (numb_of_iteration % 3 == 0) {
                int p_x, p_y;
                do {
                    p_x = ran(1, height - 1.00001);
                    p_y = ran(1, width - 1.00001);
                } while (area[p_x][p_y] != 0);
                area[p_x][p_y] = -3;
            }


            for (int i = 0; i < Bots.size(); i++) {
                if (Active_Bots[i] == 0) {
                    Bots[i].do_comm();
                    if (Bots[i].health <= 0) {
                        Curr_Bot++;
                        Active_Bots[i] = Curr_Bot;
                    }
                    /*
                    if (Bots[i].killed != {-1, -1}) {
                        Curr_Bot++;
                        Active_Bots[Bots_places[Bots[i].killed]] = Curr_Bot;
                        Bots_places[Bots[i].killed] = 0;
                        Bots[i].killed = {-1, -1};
                    }
                    Bots_places[Bots[i].x, Bots[i].y] = i;
                    */
                }
            }

            if (numb_of_iteration >= 1000) {
                cout << "YES";
            }
        }

        //-------GA place------//



        Selection(Bots, Active_Bots);
        //Uniform_Crossover(Bots);
        //Best_Crossover(Bots, Active_Bots);
        Other_Crossover(Bots);
        Mutation(Bots);
        if (numb_of_iteration > 10000) cout << numb_of_iteration << endl;

        if (numb_of_iteration > result) {
            iter = S;
        }
        result = max(result, numb_of_iteration);
    }

    cout << iter << " " << result;

    return 0;
}
