import requests
import re
import pandas as pd

def main():
    # PROVIDE BRANDS TO SEARCH FOR
    good_brands_file = 'good_brands.txt'  # text file should have one distrbutor per line

    # PROVIDE A LIST OF URLS
    list_of_distributors_urls = '2019_Exhibitors.txt' # 'distributors.txt'

    # Store brands as a list
    print("Retreiving brands from '" + good_brands_file + "'...")
    brands = set(line.strip() for line in open(good_brands_file))

    # Store URLs as a list
    print("Retreiving URLs from '" + list_of_distributors_urls + "'...")
    urls = list(line.strip() for line in open(list_of_distributors_urls))

    # Create a list for data
    data = []

    # Search each URL for brand names
    print("Searching websites for brand names...")
    for dist_url in urls:
        print("Searching '" + dist_url + "' for brand names...")
        try:
            dist_html = requests.get(dist_url).text.lower()
            hits = []
            number_of_brands = 0
            for brand in brands:
                brand = brand.lower()
                if counter(dist_html, brand) > 0:
                    hits.append(brand)
                    number_of_brands += 1
            dist_row = [dist_url, number_of_brands, hits]
            data.append(dist_row)
        except:
            print("'" + dist_url + "' failed. Skipping URL")
            pass

    # Convert results to CSV file
    print("Finished searching for brands.\nConverting results to CSV...")
    df = pd.DataFrame(data, columns=["Website", "Total", "Hits"])
    csv_name = "RateMyDistributor.csv"
    df.to_csv(csv_name)

    print("Success.  Results can be found in '" + csv_name + "'")


def counter(string, substring):
    string_size = len(string)
    substring_size = len(substring)
    count = 0
    for i in range(0, string_size - substring_size + 1):
        if string[i:i + substring_size] == substring:
            count += 1
            break # no need to actually count occurances
    return count

if __name__ == '__main__':
    main()
