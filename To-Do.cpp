#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

int main() {
    std::cout << "1. Add a task\n2. View all tasks\n3. Delete a task\n4. Exit\nEnter your choice: ";
    int choice;
    std::cin >> choice;
    std::cin.ignore(std::numeric_limits<std::streamsize>std::max(), '\n'); // Clear the input buffer

    switch(choice) {
        case 1: {
            std::string task;
            std::cout << "Enter the task: ";
            std::getline(std::cin, task); // Use getline to read a line with spaces
            std::ofstream file("tasks.txt", std::ios::app);
            file << task << std::endl;
            break;
        }
        case 2: {
            std::ifstream file("tasks.txt");
            std::string task;
            while(std::getline(file, task)) {
                std::cout << task << std::endl;
            }
            break;
        }
        case 3: {
            std::string taskToDelete;
            std::cout << "Enter the task to delete: ";
            std::getline(std::cin, taskToDelete);
            std::ifstream file("tasks.txt");
            std::vector<std::string> tasks;
            std::string line;
            while(std::getline(file, line)) {
                if(line != taskToDelete) {
                    tasks.push_back(line);
                }
            }
            file.close();
            std::ofstream outFile("tasks.txt", std::ios::trunc); // Open in truncate mode to overwrite
            for(const auto& task : tasks) {
                outFile << task << std::endl;
            }
            break;
        }
        case 4:
            return 0;
    }
    return 0;
}