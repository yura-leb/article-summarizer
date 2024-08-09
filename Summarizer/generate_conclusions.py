import os
from digest import PromptsContainer
from sys import argv

def generate_micro_conclusions(dir: str, output_filename: str):
    """
    Generate conclusions for all PDF files in the given directory.
    """

    pc = PromptsContainer()
    
    with open(output_filename, "w") as f:
        for i, filename in enumerate(os.listdir(dir)):
            if filename.endswith(".pdf"):
                # Generate a micro conclusion for the article
                conclusion = pc.apply_micro_conclusions_prompt_to_article(dir + os.sep + filename)

                f.write(str(i+1) + ": " + filename[:-4] + "\n" + conclusion + "\n\n\n")



if __name__ == "__main__":
    if len(argv) == 3:
        generate_micro_conclusions(argv[1], argv[2])
    else:
        dir = input("Enter folder name with pdfs: ")
        output_filename = input("Enter output filename: ")
        generate_micro_conclusions(dir, output_filename)
