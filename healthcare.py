import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


#Load CSV file for Analysis
def load_data(data):
    df = pd.read_csv(data)
    pd.set_option("display.max_columns", None)
    return df

#Exploratory Data Analysis
def explore_data(data):
    print("First 10 rows of dataset: \n",data.head(10))
    data.info()
    print("Dataset summary: \n", data.describe())
    print("Dataset shape: \n", data.shape)
    #rename date of admission column
    data.rename(columns={"Date of Admission": "Admission Date"}, inplace=True)
    #Identifying missing data from dataset
    print("Missing data: \n", data.isnull().sum())

    print("Unique number of patients: \n", data["Name"].nunique())

    for col in ["Gender", "Blood Type", "Medical Condition", "Doctor", "Hospital", "Insurance Provider", "Admission Type", "Medication"]:
        print(f"{col} : {data[col].unique()}")

    data["Admission Date"] = pd.to_datetime(data["Admission Date"], errors= "coerce")
    data["Discharge Date"] = pd.to_datetime(data["Discharge Date"], errors= "coerce")
    data["Length of Stay"] = data["Discharge Date"] - data["Admission Date"]
    data.info()

    print("First 10 rows of dataset: \n", data.head(10))
    data["Billing Amount"] = data["Billing Amount"].replace(r'[\$,]', '', regex = True).astype(float)
    print("Age of patient by billing amount: \n", data.groupby("Age")["Billing Amount"].sum().sort_values(ascending=False))
    print("Date of Admissions for each day: \n", data["Admission Date"].value_counts().sort_values(ascending= False))
    print("Doctors visited by patients: \n",data["Doctor"].value_counts().sort_values(ascending=False))
    print("Number of unique patients per doctor: \n", data.groupby("Doctor")["Name"].nunique().sort_values(ascending= False))

    # Check for duplicate values
    print("Duplicate rows: \n", data.duplicated().sum())
    #Dropping duplicate rows only if the combination of below columns are truly redundant
    #check the kind of duplicate data present in the dataset
    #save duplicates before dropping
    duplicates = data[data.duplicated()]
    duplicates.to_csv("duplicate_rows.csv", index=False)
    # Then drop, on safer side, dropping the duplicate rows, if the columns are truly redundant
    data.drop_duplicates(inplace=True)
    print(duplicates.head())
    print("No duplicates were found after analyzing the csv file")

    print("Hospital visited by most number of patients: \n", data.groupby("Hospital")["Name"].nunique().sort_values(ascending= False))

    #Define age range
    bins = [0, 20, 30, 40, 50, 60, 70, 80, 100]
    labels =  ['0-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '80+']

    #create a new column for age groups
    data["Age Group"] = pd.cut(data["Age"], bins = bins, labels = labels, right= True)
    total_age_group_billing = data.groupby("Age Group", observed = True)["Billing Amount"].sum().sort_index()
    avg_age_group_billing = data.groupby("Age Group", observed = True)["Billing Amount"].mean().sort_index()
    # group billing amount by age
    print("Total billing amount by age group: \n", total_age_group_billing)
    print("Average billing amount by age group: \n", avg_age_group_billing)

    #group by medical conditions i.e, patients visiting hospitals due to various conditions
    print("Hospital visit group by medical conditions: \n", data.groupby("Medical Condition")["Hospital"].value_counts().sort_values(ascending=False))
    insurance_provider_by_medical_condition_grouped_data = data.groupby(["Medical Condition", "Insurance Provider"])["Name"].count().reset_index()
    insurance_provider_by_medical_condition_grouped_data.rename(columns = {"Name" : "Patient Count"}, inplace= True)

    return total_age_group_billing, avg_age_group_billing, insurance_provider_by_medical_condition_grouped_data

# Identifying Insurance Provider to number of patients By Medical conditions
def insurance_by_medical_condition(data):
    plt.figure(figsize=(14,6))
    sns.barplot(data= data, x = "Medical Condition", y = "Patient Count", hue= "Insurance Provider")
    plt.title("Patient Count by Insurance Provider and Medical Condition")
    plt.xlabel("Medical Condition")
    plt.ylabel("Number of Patients")
    plt.xticks(rotation = 45, ha = "right")
    plt.legend(title =  "Insurance Provider", bbox_to_anchor = (1.05,1), loc = "upper left")
    plt.tight_layout()
    plt.savefig("images/insurance_by_medical_condition.png")
    plt.show()
    #Outcome : Cigna, Medicare and United Health Care are the leading Insurance Provider to maximum number of people with serious medical conditions.


# Scatter plot for hospital stay vs billing amount
def seaborn_scatter_stay_vs_billing(data):
    data = data.copy()
    # Ensure 'Length of Stay' is timedelta before extracting days
    if pd.api.types.is_timedelta64_dtype(data["Length of Stay"]):
        data["Stay Days"] = data["Length of Stay"].dt.days
    else:
        data["Stay Days"] = data["Length of Stay"]

    # Get top 5 most common medical conditions
    top_conditions = data["Medical Condition"].value_counts().nlargest(5).index
    plot_data = data[data["Medical Condition"].isin(top_conditions)]

    # clean up data
    plot_data = plot_data.dropna(subset=["Stay Days", "Billing Amount", "Age Group"])

    if len(plot_data) > 100:
        plot_data = plot_data.sample(n=100, random_state=42)

    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=plot_data, x="Stay Days", y="Billing Amount", hue="Age Group", palette='viridis', alpha=0.6,
                    s=60)
    plt.title("Length of Stay vs. Billing Amount by Age Group (100 samples)")
    plt.xlabel("Length of Stay (Days)")
    plt.ylabel("Billing Amount ($)")
    plt.legend(title="Age Group", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig("images/seaborn_scatter_stay_vs_billing.png")
    plt.show()


#plot total billing amount by age group
def plot_total_billing_by_age(data):
    plt.figure(figsize=(10,6))
    data.plot(kind = "bar", color = 'green')
    plt.title("Total Billing amount by age group")
    plt.xlabel("Age Group")
    plt.ylabel("Billing Amount")
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.savefig("images/plot_total_billing_by_age.png")
    plt.show()


#plot average billing by age group
def plot_avg_billing_by_age(data):
    plt.figure(figsize=(10,6))
    data = data.sort_index()
    data.index = data.index.astype(str)
    data.plot(linestyle = "-", marker = "o", color = 'red')
    plt.title("Average Billing amount by age group")
    plt.xlabel("Age Group")
    plt.ylabel("Billing Amount")
    plt.xticks(rotation = 45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("images/plot_avg_billing_by_age.png")
    plt.show()


#Main Program
def main():
    healthcare_raw_data = load_data("healthcare_dataset.csv")
    total_age_group_billing, avg_age_group_billing, insurance_provider_by_patient_count = explore_data(healthcare_raw_data)
    #ml_workflow(healthcare_raw_data)
    #hist_avg_billing(healthcare_raw_data)
    insurance_by_medical_condition(insurance_provider_by_patient_count)
    seaborn_scatter_stay_vs_billing(healthcare_raw_data)
    plot_total_billing_by_age(total_age_group_billing)
    plot_avg_billing_by_age(avg_age_group_billing)



if __name__ == "__main__":
    main()




