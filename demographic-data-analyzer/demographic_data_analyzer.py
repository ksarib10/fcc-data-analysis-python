import os
import pandas as pd


def calculate_demographic_data(print_data=True):
    
    # pass
    file_path = os.path.join(os.path.dirname(__file__), "adult.data")

    # Loading dataset and Adding names to the columns because there was no header in the dataset

    df = pd.read_csv(file_path, 
    names=["age", "workclass", "fnlwgt", "education", "education-num", "marital-status",
    "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
    "hours-per-week", "native-country", "salary"])


    # Strip whitespace from all object (string) columns

    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
    # Some of the values had spaces so i removed the spaces to avoid errors in future

    # 1. How many people of each race are represented
    race_count = dict(df['race'].value_counts())

    # 2. Average age of men
    avg_men_age = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # 3. Percentage with Bachelor's degree
    percentage_bachelors = round((df['education'] == 'Bachelors').sum()/df['education'].count() * 100, 1)

    # 4. Percentage of people with advanced education (Bachelors, Masters, or Doctorate) make more than 50K
    adv_edu_people = df[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]  # People with advance education
    total = adv_edu_people['salary'].count()  # Advance education people count
    earning_plus50K = (adv_edu_people['salary'] == '>50K').sum()  # people with >50K salary
    percentage_adv = round(earning_plus50K/total * 100, 1)  # their percentage


    # 5. Percentage with salary >50K by education
    not_adv_people = df[~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]  # # People without advance education
    total = not_adv_people['salary'].count()  # # No advance education people count
    earning_plus50K = (not_adv_people['salary'] == '>50K').sum()  # people with >50K salary
    percentage_nadv = round(earning_plus50K/total * 100, 1)  # their percentage


    # # 6. Minimum number of work hours per week
    min_hours = df['hours-per-week'].min()

    # 7. % rich among those who work min hours
    total_people = df[df['hours-per-week'] == min_hours]
    earning_plus50K = total_people[total_people['salary'] == '>50K']
    rich_percentage = round(len(earning_plus50K)/len(total_people) * 100, 1)

    # 8. Country with highest % of >50K
    # Method 1
    stats = df.groupby("native-country")["salary"]
    percentage_data = stats.apply(lambda x: (x == ">50K").mean())
    country, per = percentage_data.idxmax(), round(percentage_data.max()*100, 1)

    # # Method 2
    # # To have all contries in a list so that i can use it in method 2 of next question
    # countries = df['native-country'].unique().tolist()
    # df['salary'].value_counts()
    # h_percentage, h_country = 0.0, ""
    # for cntry in countries:
    #     perc = ((df['native-country'] == cntry) & (df['salary'] == '>50K')).sum()/(df['native-country'] == cntry).sum()
    #     if perc > h_percentage: h_percentage, h_country = perc, cntry
            
    # print(f"highest percentage of people that earn >50K:\nCountry: {h_country}, Percentage: {round(h_percentage*100, 2)}%") 


    # 9. Most popular occupation for >50K in India
    indians = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
    # occupation = indians['occupation'].value_counts().idxmax()
    occupation = indians['occupation'].mode()[0]

    if print_data:
        print('Races and their counts:')
        print("\n".join(f"{i}: {j}" for i, j in race_count.items()))

        print(f"\nAverage age of men: {avg_men_age}")

        print(f"\nPercentage of people who have a Bachelor's degree: {percentage_bachelors}%")

        print(f"\nPercentage of people with advanced education making more than 50K: {percentage_adv}%")
        
        print(f"\nPercentage of people without advanced education making more than 50K: {percentage_nadv}%")
        
        print(f"\nMinimum number of work hours per week: {min_hours}")
        
        print(f"\nPercentage of the people with minimum number of hours/week having salary more than 50K: {rich_percentage}%")
        
        print("\nCountry with highest percentage of people that earn >50K:")
        print(f"Country: {country}, Percentage: {per}%")

        print(f"\nThe most popular occupation for those who earn >50K in India: {occupation}\n")

    return {
        'race_count': race_count,
        'average_age_men': avg_men_age,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': percentage_adv,
        'lower_education_rich': percentage_nadv,
        'min_work_hours': min_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': country,
        'highest_earning_country_percentage': per,
        'top_IN_occupation': occupation
    }

if __name__ == "__main__":
    print(calculate_demographic_data())
