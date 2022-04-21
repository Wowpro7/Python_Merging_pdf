import PyPDF2 as pypdf2
import os


# https://www.blog.pythonlibrary.org/2018/06/07/an-intro-to-pypdf2/

def check_files_validation(first_pdf_path, second_pdf_path):
    Files_are_valid = 'True'  # this way, because walking around with booleans was too much time consuming, and its
                                                                                    # 03:16am, so deal with it_:)
    if first_pdf_path.split('.')[-1] != 'pdf':
        Files_are_valid = first_pdf_path

    if second_pdf_path.split('.')[-1] != 'pdf':
        if Files_are_valid == 'True':
            Files_are_valid = second_pdf_path
        else:
            Files_are_valid += ', ' + second_pdf_path

    return Files_are_valid


def odd_even_merge(pdf_1, pdf_2, new_pdf, first_pdfs_page=True):
    pdf_1_page_num = pdf_1.getNumPages()
    count_1 = 0
    pdf_2_page_num = pdf_2.getNumPages()
    count_2 = 0

    if pdf_1_page_num > pdf_2_page_num:  # compare files pages size to know how many times to run the loop
        run_pages = pdf_1_page_num
    else:
        run_pages = pdf_2_page_num

    for i in range(run_pages):  # run through all the pages

        if first_pdfs_page:  # if its True
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


def merge_in_sequence(pdf_1, pdf_2, new_pdf, first_pdfs_page=True):
    pdf_1_page_num = pdf_1.getNumPages()
    count_1 = 0
    pdf_2_page_num = pdf_2.getNumPages()
    count_2 = 0

    sum_pages_value = pdf_1_page_num + pdf_2_page_num

    for i in range(sum_pages_value):  # run through all the pages

        if first_pdfs_page:  # if its True start with the first pdf
            if pdf_1_page_num > count_1:
                new_pdf.addPage((pdf_1.getPage(count_1)))
                count_1 += 1

            if pdf_1_page_num == count_1:  # when finished running over all the pdf switch the "first_pdfs_pages" boolean value to continue with the other file
                first_pdfs_page = not first_pdfs_page

        else:
            if pdf_2_page_num > count_2:
                new_pdf.addPage((pdf_2.getPage(count_2)))
                count_2 += 1

            if pdf_2_page_num == count_2:  # when finished running over all the pdf switch the "first_pdfs_pages" boolean value to continue with the other file
                first_pdfs_page = not first_pdfs_page
    return new_pdf


def merge_in_the_middle(pdf_1, pdf_2, new_pdf, first_middle_pause_page, first_pdfs_page=True):
    pdf_1_page_num = pdf_1.getNumPages()
    count_1 = 0
    pdf_2_page_num = pdf_2.getNumPages()
    count_2 = 0

    if first_pdfs_page:
        if first_middle_pause_page > pdf_1_page_num:
            return None
    else:
        if first_middle_pause_page > pdf_2_page_num:
            return None

    sum_pages_value = pdf_1_page_num + pdf_2_page_num
    file_current_mering_part = 1  # it can be up tp 3 parts (starting from 1)

    for i in range(sum_pages_value):  # run through all the pages
        if file_current_mering_part == 1:
            if first_pdfs_page:  # if its True start with the first pdf
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
            if not first_pdfs_page:  # if its True start with the first pdf
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
            if first_pdfs_page:  # if its True start with the first pdf
                if pdf_1_page_num > count_1:
                    new_pdf.addPage((pdf_1.getPage(count_1)))
                    count_1 += 1

            else:
                if pdf_2_page_num > count_2:
                    new_pdf.addPage((pdf_2.getPage(count_2)))
                    count_2 += 1

    return new_pdf


def merge(first_pdf_path, second_pdf_path, first_pdfs_page, User_named=None, odd_even=None, Sequence=None,
          Middle=None, first_middle_pause_page=None):  # merger two files

    filename = check_files_validation(first_pdf_path, second_pdf_path)
    if filename != 'True':
        return "***ERROR 404 - You Fucked up, '%s' file/s is invalid ***" % filename

    if User_named is None:  # if the user asked for a specific name use it
        if first_pdfs_page:  # the first name determines the first page
            new_pdf_name = "_{0}_and_{1}.pdf".format(first_pdf_path.split('.')[0], second_pdf_path.split('.')[0])
        else:
            new_pdf_name = "_{1}_and_{0}.pdf".format(first_pdf_path.split('.')[0], second_pdf_path.split('.')[0])
    else:
        new_pdf_name = "%s.pdf" % User_named

    # basic information all functions need: - received at the function call
    pdf_1 = pypdf2.PdfFileReader(first_pdf_path)
    pdf_2 = pypdf2.PdfFileReader(second_pdf_path)
    new_pdf = pypdf2.PdfFileWriter()

    # basic information returned by all function:s
    if odd_even:  # merge page by page from different files
        new_pdf = odd_even_merge(pdf_1, pdf_2, new_pdf, first_pdfs_page)
    elif Sequence:  # sequential merge
        new_pdf = merge_in_sequence(pdf_1, pdf_2, new_pdf, first_pdfs_page)
    elif Middle:  # merge in at starting page
        new_pdf = merge_in_the_middle(pdf_1, pdf_2, new_pdf, first_middle_pause_page, first_pdfs_page)
    else:
        return "***ERROR 404 - You Fucked up, choose an option for merging***"

    if new_pdf is None:
        return "***ERROR 404 - You Fucked up, middle page value is too high***"
    else:
        with open(new_pdf_name, 'wb') as pdf:  # create the file
            new_pdf.write(pdf)
        return new_pdf_name


def main():
    # TODO:
    """
    Fixed. 1: run the code over different types of files.
    2: run the code over pdf with password.
    3: try to brut force a pdf with password and see if it is possible, if yes add the option to the code.
    4: create GUI design and implement it over the codeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee.
    """

    file_name = merge(User_named="test_sequential_merge", first_pdf_path='1.txt',
                      second_pdf_path='testing_txt.txt', first_pdfs_page=False, first_middle_pause_page=1, Middle=True)

    print("file name: '%s' , is ready for usage" % file_name)


if __name__ == '__main__':
    main()
