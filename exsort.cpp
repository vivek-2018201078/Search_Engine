#include<stdio.h>
#include<bits/stdc++.h>
#include<iostream>
#include<cstring>
#include<fstream>
#include<sstream>

using namespace std;

vector<ifstream*> fall;
int nf;

class comp {
public:
	bool operator() (const pair<string, int> &a, const pair<string, int> &b) const {
		string x = a.first.substr(0, a.first.find(':'));
		string y = b.first.substr(0, b.first.find(':'));
		if(x > y)
			return true;
		return false;
	}
};

priority_queue<pair<string, int>, vector<pair<string, int>>, comp> pq;


int main(int argc, char const *argv[])
{
    string index_folder = argv[1];
    ifstream nooffiles;
    ofstream outfile (index_folder + "/final.txt");
    nooffiles.open(index_folder + "/no_of_files.txt");
    nooffiles >> nf;
    nooffiles.close();
	for(int i = 0; i < nf; i++) {
		ifstream* f = new ifstream((index_folder + "/file" + to_string(i) + ".txt").c_str() );
		fall.push_back(f);
	}

	string line;
	for(int i = 0; i < fall.size(); i++) {
		//cout << i << "th file" << "\n";
		if(getline(*fall[i], line)) {
		    //cout << line << "\n";
			pq.push({line, i});
		}
	} 

    string prev_word = "";
    string prev_post_list = "";
	while(!pq.empty()) {
		pair<string, int> temp = pq.top();
		pq.pop();
		string word = temp.first.substr(0, temp.first.find(':'));
		string post_list = temp.first.substr(temp.first.find(':') + 1);
		if(!prev_word.empty() && prev_word == word) {
		    //cout << "here\n";
		    prev_post_list = prev_post_list + "|" + post_list;
		}
		else {
		    //insert into file
		    if(!prev_word.empty()) {
		        outfile << prev_word << ":" << prev_post_list << "\n";
		        prev_post_list = "";
		    }
            prev_word = word;
		}
		if(prev_post_list.empty()) {
		    prev_post_list = post_list;
		}
		//cout << word << " " << post_list << "\n";
		//cout << temp.first << "   " << temp.second <<"\n";
		int filenum = temp.second;
		if(getline(*fall[filenum], line)) {
			pq.push({line, filenum});
		}
	}
	if(!prev_word.empty())
        outfile << prev_word << ":" << prev_post_list << "\n";
    outfile.close();
    for(int i = 0; i < nf; i++) {
        string filename = index_folder + "/file" + to_string(i) + ".txt";
        remove(filename.c_str());
    }

	return 0;
}