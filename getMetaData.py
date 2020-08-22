__author__ = "Ashad Nadeem Mahmudi"
__date__ = "8/22/2020"

from bs4 import BeautifulSoup
import requests
import re
import csv

Title = list()
Rating = list()
Price = list()

def visitSite(links):
    """Visits the Udemy Website for the course and Get the Meta Data for each Course link provided
    :returns List of Title , Price and Rating
    """
    for i,url in enumerate(links):
        soup = BeautifulSoup(requests.get(url).content, "html.parser")

        # Gets The Title of the Course
        print("Visiting Course {}".format(i))
        Title.append(soup.find("h1").find(text=True).strip())

        for span_tags in soup.find_all("span"):
            text = span_tags.find(text=True)
            if text != None :
                if re.match(r"\$", text):
                    # print("Original Price: {}".format(text))
                    Price.insert(i, text)
                rat = re.match(r"^Rating: (.*) out of 5$", text)
                if rat:
                    # print("Rating :{}".format(rat.group(1)))
                    Rating.insert(i, rat.group(1))
    return Title, Price, Rating

def print_table(t,p,r):
    """Prints Title Price and Rating of the courses"""
    for i , Title in enumerate(t):
        print(Title,end=", ")
        print(p[i],end=", ")
        print(r[i])

def readLinks(filename):
    """Read Links from txt file, Take FileName as Parameter"""
    with open(filename, "r") as file:
        courses = file.readlines()
    print("Reading Courses from File")
    return courses

def write_csv(t, p, r):
    """Write Title Price and Rating of the course to Csv File"""

    with open("Courses.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        for i, Title in enumerate(t):
            row = [Title, p[i], r[i]]
            writer.writerow(row)
    print("Writing Csv")

if __name__ == '__main__':

    courseLinks = readLinks("UdemyLinks.txt")
    Title,Price,Rating = visitSite(courseLinks)
    print_table(Title, Price, Rating)
    write_csv(Title, Price, Rating)