import PyPDF2 as pypdf2
import os


# import pikepdf # alternative to pypdf2

MERGING_STYLES_LIST = ['Sequence', 'Middle Merger', 'Odd - Even', 'Cut']


def check_files_type_validity(first_pdf_path=None, second_pdf_path=None):
    Files_are_valid = 'True'  # this way, because walking around with booleans was too much time consuming, and its
    # 03:16am, so deal with it_:)
    if first_pdf_path is not None:
        if not first_pdf_path.endswith('.pdf'):
            Files_are_valid = first_pdf_path

    if second_pdf_path is not None:
        if not second_pdf_path.endswith('.pdf')  :
            if Files_are_valid == 'True':
                Files_are_valid = second_pdf_path
            else:
                Files_are_valid += ', ' + second_pdf_path

    return Files_are_valid


def check_files_accessibility(first_pdf_path, second_pdf_path): #
    temp_dict = {"first_pdf_path": None, "first_pdf_pages_num": None, "second_pdf_path": None, "second_pdf_pages_num": None}
    Error_message = None
    try:
        try:
            if first_pdf_path is not None:
                temp_dict["first_pdf_path"] = pypdf2.PdfFileReader(first_pdf_path)
                temp_dict["first_pdf_pages_num"] = temp_dict["first_pdf_path"].getNumPages()
        except pypdf2.utils.PdfReadError:
            Error_message = first_pdf_path
        finally:  # even if the first exception occurs always check the second file
            try:
                if second_pdf_path is not None:
                    temp_dict["second_pdf_path"] = pypdf2.PdfFileReader(second_pdf_path)
                    temp_dict["second_pdf_pages_num"] = temp_dict["second_pdf_path"].getNumPages()
            except pypdf2.utils.PdfReadError: # both paths are not accessible, create an Error message
                if temp_dict["first_pdf_path"] is None:
                    Error_message += second_pdf_path + ', '
                else:
                    Error_message = second_pdf_path
                Error_message = Error_message + ', this file/s might be broken or password protected'

        return temp_dict, Error_message
    except FileNotFoundError as exp:
        return temp_dict, str(exp)


def create_new_file_name (User_named, first_pdf_leads, first_pdf_path, second_pdf_path):
    if User_named is None:  # if the user asked for a specific name use it
        if first_pdf_leads:  # the first name determines the first page
            return "_{0}_and_{1}.pdf".format(first_pdf_path.split('.')[0], second_pdf_path.split('.')[0])
        else:
            return"_{1}_and_{0}.pdf".format(first_pdf_path.split('.')[0], second_pdf_path.split('.')[0])
    else:
        return "%s.pdf" % User_named


def odd_even_merge(pdf_1, pdf_1_page_num, pdf_2, pdf_2_page_num, new_pdf, first_pdf_leads=True):
    count_1 = 0
    count_2 = 0

    if pdf_1_page_num > pdf_2_page_num:  # compare files pages size to know how many times to run the loop
        run_pages = pdf_1_page_num
    else:
        run_pages = pdf_2_page_num

    for i in range(run_pages):  # run through all the pages

        if first_pdf_leads:  # if its True
            if pdf_1_page_num > count_1:
                new_pdf.addPage((pdf_1.getPage(count_1)))
                count_1 += 1
            if pdf_2_page_num > count_2:
                new_pdf.addPage((pdf_2.getPage(count_2)))
                count_2 += 1

        else:
            if pdf_2_page_num > count_2:
                new_pdf.addPage((pdf_2.getPage(count_2)))
                count_2 += 1
            if pdf_1_page_num > count_1:
                new_pdf.addPage((pdf_1.getPage(count_1)))
                count_1 += 1
    return new_pdf


def merge_in_sequence(pdf_1, pdf_1_page_num, pdf_2, pdf_2_page_num, new_pdf, first_pdf_leads=True):
    count_1 = 0
    count_2 = 0

    sum_pages_value = pdf_1_page_num + pdf_2_page_num

    for i in range(sum_pages_value):  # run through all the pages

        if first_pdf_leads:  # if its True start with the first pdf
            if pdf_1_page_num > count_1:
                new_pdf.addPage((pdf_1.getPage(count_1)))
                count_1 += 1

            if pdf_1_page_num == count_1:  # when finished running over all the pdf switch the "first_pdf_leadss" boolean value to continue with the other file
                first_pdf_leads = not first_pdf_leads

        else:
            if pdf_2_page_num > count_2:
                new_pdf.addPage((pdf_2.getPage(count_2)))
                count_2 += 1

            if pdf_2_page_num == count_2:  # when finished running over all the pdf switch the "first_pdf_leadss" boolean value to continue with the other file
                first_pdf_leads = not first_pdf_leads
    return new_pdf


def merge_in_the_middle(pdf_1, pdf_1_page_num, pdf_2, pdf_2_page_num, new_pdf, first_middle_pause_page,
                        first_pdf_leads=True):
    count_1 = 0
    count_2 = 0

    if first_pdf_leads:
        if first_middle_pause_page > pdf_1_page_num:
            return None
    else:
        if first_middle_pause_page > pdf_2_page_num:
            return None

    sum_pages_value = pdf_1_page_num + pdf_2_page_num
    file_current_mering_part = 1  # it can be up tp 3 parts (starting from 1)

    for i in range(sum_pages_value):  # run through all the pages
        if file_current_mering_part == 1:
            if first_pdf_leads:  # if its True start with the first pdf
                if first_middle_pause_page > count_1:
                    new_pdf.addPage((pdf_1.getPage(count_1)))
                    count_1 += 1

                if first_middle_pause_page == count_1:
                    file_current_mering_part = 2

            else:
                if first_middle_pause_page > count_2:
                    new_pdf.addPage((pdf_2.getPage(count_2)))
                    count_2 += 1

                if first_middle_pause_page == count_2:
                    file_current_mering_part = 2

        elif file_current_mering_part == 2:
            if not first_pdf_leads:  # if its True start with the first pdf
                if pdf_1_page_num > count_1:
                    new_pdf.addPage((pdf_1.getPage(count_1)))
                    count_1 += 1

                if pdf_1_page_num == count_1:
                    file_current_mering_part = 3

            else:
                if pdf_2_page_num > count_2:
                    new_pdf.addPage((pdf_2.getPage(count_2)))
                    count_2 += 1

                if pdf_2_page_num == count_2:
                    file_current_mering_part = 3

        elif file_current_mering_part == 3:
            if first_pdf_leads:  # if its True start with the first pdf
                if pdf_1_page_num > count_1:
                    new_pdf.addPage((pdf_1.getPage(count_1)))
                    count_1 += 1

            else:
                if pdf_2_page_num > count_2:
                    new_pdf.addPage((pdf_2.getPage(count_2)))
                    count_2 += 1

    return new_pdf


def merge_cut_pages_off(pdf_1, pdf_1_page_num, first_middle_pause_page, stop_page, new_pdf):
    for i in range(first_middle_pause_page, stop_page+1):
        new_pdf.addPage((pdf_1.getPage(i)))

    return new_pdf


def define_merging_style(merging_style):
    odd_even = None
    Sequence = None
    Middle = None
    cut = None

    for i in merging_style.keys():
        if i == 'Sequence':
            Sequence = merging_style[i]
        elif i == 'Middle Merger':
            Middle = merging_style[i]
        elif i == 'Odd - Even':
            odd_even = merging_style[i]
        elif i == 'Cut':
            cut = merging_style[i]

    return odd_even, Sequence, Middle, cut


#def merge(first_pdf_path, second_pdf_path, saving_path=None, first_pdf_leads=True, User_named=None, odd_even=None, Sequence=None,
        #  Middle=None, first_middle_pause_page=None):  # merger two files.. Previous version before the use of tuple

def merge(first_pdf_path, second_pdf_path, saving_path=None, first_pdf_leads=True, User_named=None, merging_style={}, first_middle_pause_page=None, stop_page=None):  # merger two files

    odd_even, Sequence, Middle, cut = define_merging_style(merging_style)

    filename = check_files_type_validity(first_pdf_path, second_pdf_path)
    if filename != 'True':
        return "*** '%s' file/s is invalid ***" % filename

    # basic information all functions need: - received at the function call
        # checking for file validation for use
    file_access, Error_message = check_files_accessibility(first_pdf_path, second_pdf_path)
    if Error_message is not None:
        return Error_message
    else:
        pdf_1 = file_access["first_pdf_path"]
        pdf_1_page_num = file_access["first_pdf_pages_num"]
        pdf_2 = file_access["second_pdf_path"]
        pdf_2_page_num = file_access["second_pdf_pages_num"]

    new_pdf = pypdf2.PdfFileWriter()

    # basic information returned by all function:s
    if odd_even:  # merge page by page from different files
        new_pdf = odd_even_merge(pdf_1, pdf_1_page_num, pdf_2, pdf_2_page_num, new_pdf, first_pdf_leads)
    elif Sequence:  # sequential merge
        new_pdf = merge_in_sequence(pdf_1, pdf_1_page_num, pdf_2, pdf_2_page_num, new_pdf, first_pdf_leads)
    elif cut:  # cut pages from the original pdf file and create an new file
        if first_middle_pause_page > pdf_1_page_num or first_middle_pause_page > stop_page:
            return 'Error: Starting page is bigger than the number of pages available'

        if first_middle_pause_page > stop_page:
            return 'Error: Starting page is bigger than the Stop page'

        if stop_page > pdf_1_page_num:
            return 'Error: Stop page is bigger than the number of pages available'

        new_pdf = merge_cut_pages_off(pdf_1, pdf_1_page_num,first_middle_pause_page , stop_page, new_pdf)
    elif Middle:  # merge in at starting page
        if first_pdf_path:
            if pdf_1_page_num < first_middle_pause_page:
                return "Middle page pause value is too high"
            elif first_middle_pause_page == 0:
                return "start page cant be 1"
        else:
            if pdf_2_page_num < first_middle_pause_page:
                return "Middle page pause value is too high"

        new_pdf = merge_in_the_middle(pdf_1, pdf_1_page_num, pdf_2, pdf_2_page_num, new_pdf, first_middle_pause_page,
                                      first_pdf_leads)
    else:
        return "***ERROR 404 - You Fucked up, choose an option for merging***"

    new_pdf_name = create_new_file_name(User_named, first_pdf_leads, first_pdf_path, second_pdf_path)
    # new_pdf.encrypt(user_pwd="123", owner_pwd="123", use_128bit=True)
    try:
        with open(saving_path+new_pdf_name, 'wb') as pdf:  # create the file
            new_pdf.write(pdf)
    except PermissionError as exp:
        return str(exp) +'\n choose a different saving path'
    except FileNotFoundError:
        return 'Your saving path is invalid, please try a different path'
    else:
        return new_pdf_name

# TODO:
"""
make the code better looking
"""

# def main():
#
#
#     file_name = merge(User_named="yea_boio", first_pdf_path="test.txt", second_pdf_path='SignalTap 2.pdf', first_pdf_leads=False, first_middle_pause_page=2, Middle=True)
#
#     print("file name: '%s' , is ready for usage" % file_name)
#
#
# if __name__ == '__main__':
#     main()
