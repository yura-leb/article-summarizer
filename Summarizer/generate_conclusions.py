import os
from PromptsContainer import PromptsContainer
from sys import argv

def generate_micro_conclusions(dir: str, output_filename: str):
    """
    Generate conclusions for all PDF files in the given directory.
    """

    pc = PromptsContainer()
    
    i = 1
    with open(output_filename, "w") as f:
        # for i, filename in enumerate(os.listdir(dir)):
        #     if filename.endswith(".pdf"):
        #         # Generate a micro conclusion for the article
        #         conclusion = pc.apply_micro_conclusions_prompt_to_article(dir + os.sep + filename)
        with open(dir + os.sep + "articles.txt", "r") as fin:
            for line in fin:
                title = line.strip()
                link = fin.readline().strip()
                print(link)
                _ = fin.readline()

                pdf_file = dir + os.sep + title + ".pdf"

                # Generate a micro conclusion for the article
                conclusion = pc.apply_micro_conclusions_prompt_to_article(pdf_file)
 
                f.write(
                    str(i) + ": " + title + "\n" + link + "\n" + conclusion + "\n\n\n"
                )
                i += 1


if __name__ == "__main__":
    if len(argv) == 3:
        generate_micro_conclusions(argv[1], argv[2])
    else:
        dir = input("Enter folder name with pdfs: ")
        output_filename = input("Enter output filename: ")
        generate_micro_conclusions(dir, output_filename)
