/*

Node 1 deatils dont print
leave a few cold pages in node 0
print the desired count of cold pages before and after.

*/

#include <bits/stdc++.h>
#include <cstdlib>
#include <ctime>
using namespace std;

// Structure of Sampled Pages
struct SampledPages
{
    string pageID;
    long long size;
    int HitNumber;
};
bool compareTwoPages(SampledPages a, SampledPages b)
{
    // returns true for higher hit number
    return a.HitNumber >= b.HitNumber;
}
string gen_random(const int len)
{
    static const char alphanum[] =
        "abcdefghijkl";
    std::string tmp_s;
    tmp_s.reserve(len);

    for (int i = 0; i < len; ++i)
    {
        tmp_s += alphanum[rand() % (sizeof(alphanum) - 1)];
    }

    return tmp_s;
}
string gen_random1(const int len)
{
    static const char alphanum[] =
        "mnopqrstuvwxyz";
    std::string tmp_s;
    tmp_s.reserve(len);

    for (int i = 0; i < len; ++i)
    {
        tmp_s += alphanum[rand() % (sizeof(alphanum) - 1)];
    }

    return tmp_s;
}
string rannum()
{
    int i;
    i = (rand() % 6) + 1;
    string s = to_string(i);
    return s;
}
int partition(vector<SampledPages> &values, int left, int right)
{
    int pivotIndex = left + (right - left) / 2;
    int pivotValue = values[pivotIndex].HitNumber;
    int i = left, j = right;
    int temp;
    while (i <= j)
    {
        while (values[i].HitNumber > pivotValue)
        {
            i++;
        }
        while (values[j].HitNumber < pivotValue)
        {
            j--;
        }
        if (i <= j)
        {
            swap(values[i], values[j]);
            i++;
            j--;
        }
    }
    return i;
}
void quicksort(vector<SampledPages> &values, int left, int right)
{
    if (left < right)
    {
        int pivotIndex = partition(values, left, right);
        quicksort(values, left, pivotIndex - 1);
        quicksort(values, pivotIndex, right);
    }
}
int main()
{
    fstream newfile;
    newfile.open("one.txt", ios::in);
    if (newfile.is_open())
    {
        string tp;
        while (getline(newfile, tp))
        {
            cout << tp << "\n";
        }
        newfile.close();
    }
    cout << "\n";
    newfile.open("two.txt", ios::in);
    if (newfile.is_open())
    {
        string tp;
        while (getline(newfile, tp))
        {
            cout << tp << "\n";
        }
        newfile.close();
    }
    vector<SampledPages> TLB1;
    vector<SampledPages> TLB2;
    cout << "\n\n";
    string page1 = "0x05: data TLB";
    long long page1_size = 4000; // all page size units are in KB
    int page1_Hit_Number = 32;
    string page2 = "0xb1: data TLB";
    long long page2_size = 2000;
    int page2_Hit_Number = 8;

    // Sampling pages into sizes of 2KB
    while (page1_size > 0)
    {
        string name = "0" + gen_random(2) + rannum();
        TLB1.push_back({name,
                        2,
                        page1_Hit_Number});
        page1_size -= 2;
    }
    while (page2_size > 0)
    {
        string name = "0" + gen_random1(2) + rannum();
        TLB2.push_back({name,
                        2,
                        page2_Hit_Number});
        page2_size -= 2;
    }

    // Representing TLB after Sampling

    cout << "TLB Node 0 After Sampling \n";
    cin.get();
    cout << "Page ID\t : Page Size : Hit Number\n";
    for (auto itr : TLB1)
    {
        cout << itr.pageID << " : " << itr.size << "K : " << itr.HitNumber << '\n';
    }
    cin.get();
    // cout << "TLB Node 1 After Sampling \n";
    // cin.get();
    // cout << "Page ID\t : Page Size : Hit Number\n";
    // for (auto itr : TLB2)
    // {
    //     cout << itr.pageID << " : " << itr.size << "K : " << itr.HitNumber << '\n';
    // }
    // cin.get();
    cout << "Injecting Cold Pages into the TLB Node 0\n\n\n";
    // Injecting 10 Cold Pages with Hit_Number 2
    for (int i = 0; i < 10; i++)
    {
        TLB1.push_back({"0x01: data TLB",
                        2,
                        2});
    }
    // Injecting 10 Cold Pages with Hit_Number 4
    for (int i = 0; i < 10; i++)
    {
        TLB1.push_back({"0x02: data TLB",
                        2,
                        4});
    }
    // Injecting 10 Cold Pages with Hit_Number 8
    for (int i = 0; i < 10; i++)
    {
        TLB1.push_back({"0x03: data TLB",
                        2,
                        8});
    }
    cout << "TLB Node 0 after injecting Cold Pages\n\n\n";
    cin.get();
    cout << "Page ID\t : Page Size : Hit Number\n";
    for (auto itr : TLB1)
    {
        cout << itr.pageID << " : " << itr.size << "K : " << itr.HitNumber << '\n';
    }
    cin.get();
    // Sorting Pages in the TLB based on Hit Number
    cout << "Sorting Sampled Pages on basis of Hit Number\n";
    quicksort(TLB1, 0, TLB1.size() - 1);
    quicksort(TLB2, 0, TLB2.size() - 1);
    cin.get();
    cout << "TLB Node 0\n";
    cout << "Page ID\t : Page Size : Hit Number\n";
    int coldcount=0;
    for (auto itr : TLB1)
    {
        cout << itr.pageID << " : " << itr.size << "K : " << itr.HitNumber << '\n';
        if(itr.HitNumber<=16)
        {
            coldcount++;
        }
    }
    cout<<"\n";
    cout<<"Count of cold Pages before swapping between nodes :"<<coldcount<<"\n\n";

    int threshold = 16;
    // cout<<"\n Enter Threshold for Hit Number\n ";
    // cin>>threshold;
    cout << "TLB size for Node 0 ( Number of Sampled Pages for Node 0 ): " << TLB1.size() << "\n";
    // cout << "TLB size for Node 1 ( Number of Sampled Pages for Node 1 ): " << TLB2.size() << "\n";
    cin.get();

    cout << "Swapping Pages between Node 0 and Node 1 based on threshold = " << threshold << " for hit number\n";
    int count=0;
    for (auto itr = TLB1.begin(); itr != TLB1.end(); itr++)
    {
        auto val = *itr;
        if (val.HitNumber < threshold)
        {
            if(count>=25)
            {
                break;
            }
            count++;
            TLB1.erase(itr);
            TLB2.push_back(val);
            itr--;
        }
    }
    for (auto itr = TLB2.begin(); itr != TLB2.end(); itr++)
    {
        auto val = *itr;
        if (val.HitNumber >= threshold)
        {
            TLB2.erase(itr);
            TLB1.push_back(val);
            itr--;
        }
    }
    cin.get();
    cout << "TLB Node 0 size ( Number of Sampled Pages ): " << TLB1.size() << "\n";
    // cout << "TLB Node 1 size ( Number of Sampled Pages ): " << TLB2.size() << "\n";
    cout << "TLB Node 0 After Swapping the pages with Hit Number Less than the threshold\n";
    cin.get();
    cout << "Page ID\t : Page Size : Hit Number\n";
    coldcount=0;
    for (auto itr : TLB1)
    {
        cout << itr.pageID << " : " << itr.size << "K : " << itr.HitNumber << '\n';
        if(itr.HitNumber<=16)
        {
            coldcount++;
        }

    }
    cout<<"\n";
    cout<<"Count of cold Pages after swapping between nodes :"<<coldcount<<"\n";
    // cout << "TLB Node 1 After Swapping the pages with Hit Number greater than the threshold\n";
    // cin.get();
    // cout << "Page ID\t : Page Size : Hit Number\n";
    // for (auto itr : TLB2)
    // {
    //     cout << itr.pageID << " : " << itr.size << "K : " << itr.HitNumber << '\n';
    // }

    return 0;
}
