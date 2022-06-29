import re
import os


def listToString(lines):
    """
    Convert list of lines into a single string object

        Parameters:
            lines (list): text where each line is a list element

        Returns:
            text (str): text where all lines are combined in one string object
    """
    text = ""
    for line in lines:
        text += line
    return text


def cleanup(text):
    """
    Cleans up text by deleating header, xml markup etc.

            Parameters:
                text (str): text with xlm markup

            Returns:
                text_clean (str): text without xlm markup
    """
    # delete header
    text_clean = re.sub(
        f"<teiHeader>.*?</teiHeader>",
        "",
        text,
        flags=re.DOTALL,
    )

    # delete xml markup tags (delete everything between "<" and ">")
    text_clean = re.sub(f"<.*?>", "", text_clean, flags=re.DOTALL)

    # delete tabs
    text_clean = text_clean.replace("\t", "")

    # delete line breaks at the beginning and end of the text
    text_clean = text_clean.replace("\n\n\n", "")
    text_clean = text_clean.replace("\n\n", "\n")

    return text_clean


def replace_tags(
    input_folder_dirs,
    modes,
    output_input_folder_dir,
    filenames=None,
    conduct_cleanup=False,
):
    """
    Main function for replacing tags in text.

        Parameters:
                input_folder_dirs (str, list): Name/Path of the input folder(s)
                modes (str, list): Signals what tag(s) should be kept (orig, reg)
                output_input_folder_dir (str): Name/Path of the output folder
                filenames (str, list): Name(s) of single files, where tag replacement should be applied to
                conduct_cleanup: If set to True it deletes all xlm markup

        Returns:
                no return values. Saves edited texts in output folder
    """
    print("Starting replacement process...")

    # looping over all input folders
    for input_folder_dir in input_folder_dirs:

        if filenames is None:
            # consider all files in folder if no filenames are provided
            filenames = os.listdir(input_folder_dir)
        elif isinstance(filenames, str):
            # convert filenames to list, if only one fileneme (as astring) is provided
            filenames = [filenames]

        # filter only for ".txt" files
        filenames = [x for x in filenames if x.endswith(".txt")]

        # convert modes to list, if only one mode (as a string) is provided
        if isinstance(modes, str):
            modes = [modes]

        # loop over all files
        for filename in filenames:
            try:
                # loop over all modes
                for mode in modes:

                    # create file dir out of folder and filename
                    file_dir = os.path.join(input_folder_dir, filename)

                    # read in all lines from ".txt" file
                    with open(file_dir) as f:
                        lines = f.readlines()

                    # convert list of lines into single string object
                    text_raw = listToString(lines)

                    # when mode is "reg", replace "orig" and ther other way around
                    replace_dict = {"reg": "orig", "orig": "reg"}

                    # look up replace tag for the mode in dictionary
                    replace_tag = replace_dict.get(mode)

                    # delete all the content between the replace_tag pair (replace with "")
                    text_replaced = re.sub(
                        f"<{replace_tag}>.*?</{replace_tag}>",
                        "",
                        text_raw,
                        flags=re.DOTALL,
                    )

                    # cleanup ".txt" file (delete header, xml tags etc.)
                    if conduct_cleanup:
                        text_replaced = cleanup(text_replaced)

                    # set mode as suffix
                    suffix = mode

                    # set output folder dir
                    filename_output = f"{filename}_{suffix}.txt"
                    file_output_dir = os.path.join(
                        output_input_folder_dir, filename_output
                    )

                    # save (write) file to output folder
                    with open(file_output_dir, "w") as f:
                        f.write(text_replaced)
            except Exception as e:
                # print name of failed file
                print(f"Failed for file {filename}")

                # print error message
                print(e)

    print("Done!")


# This is the main script, where the functions on top are called
if __name__ == "__main__":
    # list with the name(s) of the folder(s) where the raw ".txt" files are placed
    input_folder_dirs = ["Input"]

    # list of the tag(s) that should be kept
    modes = ["reg", "orig"]

    # name/path of the folder where edited texts should be saved to
    output_input_folder_dir = "Output"

    # call of the replacement function
    replace_tags(
        input_folder_dirs, modes, output_input_folder_dir, conduct_cleanup=True
    )
