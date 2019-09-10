#include<stdio.h>
#include<bits/stdc++.h>
#include<iostream>
#include<cstring>
#include<fstream>
#include<sstream>
#include<string>

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

    cout << "merging intermediate files..\n";
    string index_folder = argv[1];
    //string merge_folder = "/media/vivek/Dev/merged";
    ifstream nooffiles;
    //ofstream outfile (index_folder + "/final.txt");
    nooffiles.open(index_folder + "/no_of_files.txt");
    nooffiles >> nf;
    nooffiles.close();
    cout << "no of files = " << nf << "\n";
	for(int i = 0; i < nf; i++) {
		ifstream* f = new ifstream((index_folder + "/file" + to_string(i) + ".txt").c_str() );
		fall.push_back(f);
	}
	cout << "file pointers created\n";
	string line;
	for(int i = 0; i < fall.size(); i++) {
		//cout << i << "th file" << "\n";
		if(getline(*fall[i], line)) {
		    //cout << i << "\n";
			pq.push({line, i});
		}
		else {
			cout << "INITIAL ERROR\n";
		}
	} 
	cout << "initial 1 file pushed in pq\n";
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
		       	ofstream temp_file;
				string temp_file_name = index_folder + "/" + prev_word.substr(0, 2) + ".txt";
				//cout << temp_file_name << "\n";
			    temp_file.open(temp_file_name.c_str(), ios::app);
			    if(!temp_file) {
			     	cout << "File Error " << temp_file_name << "\n";
			    }
		        //outfile << prev_word << ":" << prev_post_list << "\n";
		        //cout << prev_word << "\n";
		        temp_file << prev_word << ":" << prev_post_list << "\n";
		        //cout << "inserted\n";
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
	if(!prev_word.empty()) {
		ofstream temp_file;
		string temp_file_name = index_folder + "/" + prev_word.substr(0, 2) + ".txt";
	    temp_file.open(temp_file_name, ios::app);
	    if(!temp_file) {
			     	cout << "File Error " << temp_file_name << "\n";
		}
        //outfile << prev_word << ":" << prev_post_list << "\n";
        temp_file << prev_word << ":" << prev_post_list << "\n";
    }
     for(int i = 0; i < nf; i++) {
         string filename = index_folder + "/file" + to_string(i) + ".txt";
         remove(filename.c_str());
     }
    cout << "Done\n";
	return 0;
}