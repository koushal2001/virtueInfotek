#include <bits/stdc++.h>
#include <cstdlib>
#include <ctime>
//jjkljkhuj
using namespace std;
string gen_random(const int len)
{
    static const char alphanum[] =
        "0123456789"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz";
    std::string tmp_s;
    // srand((unsigned)time(0));
    tmp_s.reserve(len);

    for (int i = 0; i < len; ++i)
    {
        tmp_s += alphanum[rand() % (sizeof(alphanum) - 1)];
    }

    return tmp_s;
}
int main(){
	for(int i=0;i<10;i++)
    {
        cout<<gen_random(2)<<"\n";
    }
	return 0;
}
