#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h> // Include for access function

#define MAX_FILE_SIZE 1026
#define SIGNATURE_COUNT 1000

char *virus_signatures[SIGNATURE_COUNT] = {
    "love you",
    "your bank account has been hacked ",
    "malware_signature_3"
};

int scan_file(const char *filename, int scan_mode) {
    FILE *file;
    char buffer[MAX_FILE_SIZE];
    int i;
    int malware_found = 0; // Flag to indicate if malware is found

    // Check if the file exists
    if (access(filename, F_OK) != 0) {
        printf("File not found: '%s'\n", filename);
        return -1; // Return -1 to indicate error
    }

    // Check file extension
    const char *file_extension = strrchr(filename, '.');
    if (file_extension == NULL || (strcmp(file_extension, ".badfile") != 0 && strcmp(file_extension, ".exe") != 0 && strcmp(file_extension,".py") != 0)) {
        printf("File '%s' is safe.\n", filename);
        return 0; // Return 0 to indicate safe file
    }

    // Open the file for reading
    file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error: Unable to open the file '%s'\n", filename);
        return -1; // Return -1 to indicate error
    }

    // Read the contents of the file into the buffer
    size_t bytes_read = fread(buffer, 1, MAX_FILE_SIZE, file);
    fclose(file);

    if (bytes_read == 0) {
        printf("File '%s' is empty or cannot be read.\n", filename);
        return -1; // Return -1 to indicate error``
    }

    // Check for malware in the buffer
    for (i = 0; i < SIGNATURE_COUNT; i++) {
        if (strstr(buffer, virus_signatures[i]) != NULL) {
            malware_found = 1;
            // If malware signature is found, prompt the user for the type of malware
            printf("Malware '%s' found in file '%s'\n", virus_signatures[i], filename);
            // Prompt the user if they want to see the type of malware
            char response[4];
            printf("Do you want to see the type of malware? (yes/no): ");
            scanf("%3s", response);
        
            if (strcmp(response, "yes") == 0) {
                // Identify the type of malware based on keywords in the file
                FILE *file = fopen(filename, "r");
                if (file != NULL) {
                    char line[MAX_FILE_SIZE];
                    int found = 0;
                    while (fgets(line, sizeof(line), file) != NULL) {
                        if (strstr(line, "adware") != NULL) {
                            printf("Adware malware found in file '%s'\n", filename);
                            found = 1;
                        }
                        if (strstr(line, "your bank account has been hacked") != NULL) {
                            printf("Crypto jacking malware found in file '%s'\n", filename);
                            found = 1;
                        }
                        if (strstr(line, "malicious") != NULL) {
                            printf("Malicious malware found in file '%s'\n", filename);
                            found = 1;
                        }
                        if (strstr(line, "operate") != NULL) {
                            printf("Botnet or spyware malware found in file '%s'\n", filename);
                            found = 1;
                        }
                    }
                    fclose(file);
                    if (!found) {
                        printf("Unknown malware found in file '%s'\n", filename);
                    }
                } else {
                    printf("Error: Unable to open the file '%s'\n", filename);
                }
            }

            // Prompt the user for choice to delete the file or remain it
            int choice;
            while (1) {
                printf("Enter 3 to secure your system from malware, or 4 to remain the file: ");
                scanf("%d", &choice);

                if (choice == 3) {
                    if (remove(filename) == 0) {
                        printf("File '%s' deleted successfully.\n", filename);
                    } else {
                        printf("Error: Unable to delete the file '%s'.\n", filename);
                    }
                    break;
                } else if (choice == 4) {
                    printf("File '%s' remained as usual.\n", filename);
                    break;
                } else {
                    printf("Invalid choice. Please try again.\n");
                }
            }

            break; // Stop checking further signatures
        }
    }

    // Print appropriate message if no malware signature is found
    if (!malware_found) {
        printf("No malware found in file '%s'\n", filename);
    }

    return malware_found; // Return 1 if malware found, 0 otherwise
}

// Function to prompt the user for file scanning
void scanning() {
    int num_files;
    printf("How many files do you want to scan? ");
    scanf("%d", &num_files);

    for (int i = 0; i < num_files; i++) {
        char filename[100];
        int scan_mode;

        // Prompt the user to enter the filename
        printf("Enter the name of file %d to scan: ", i + 1);
        scanf("%s", filename);

        // Check if the file exists
        if (access(filename, F_OK) != 0) {
            printf("File not found: '%s'\n", filename);
            continue; // Move to the next iteration
        }

        // Scan the file for viruses
        scan_file(filename, scan_mode);
    }
}

// Function to prompt the user for file scanning choice
void user() {
    int b;
    printf("       ANTI VIRUS SCANNER \n");
    printf("To run the scanning of file, press 1: \n");
    scanf("%d", &b);

    if (b == 1) {
        scanning();
    } else {
        printf("Invalid choice. Please try again.\n");
    }
}

int main() {
    user();
    printf("Thank you for using the virus scanner.\n");
    return 0;
}