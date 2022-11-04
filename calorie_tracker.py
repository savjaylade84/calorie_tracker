from dataclasses import dataclass
import json
import numpy as np
import matplotlib.pyplot as plt

# default goals
CALORIE_GOAL_LIMIT = 3000 # in kcal
PROTEIN_GOAL = 180 # in grams
FAT_GOAL = 80 # in grams
CARBS_GOAL = 300 # in grams

today = []


@dataclass
class Food:
	name: str
	calories: int
	protein: int
	fat: int
	carbs: int



def border() -> None:
	print(f'\n{"#" * 70}\n')

def header(title:str) -> None:
	hr = f'{"#" * 21}{"#" * len(title)}{"#" * 31}'
	print('\n' + hr)
	print(f'{"#" * 20} {title} {"#" * 30}')
	print(hr + '\n')

def get_int(message:str) -> int:
	temp = int(get_value(message))
	if temp < 0:
		return 0
	return temp

def get_value(message:str) -> str:
	temp = input(f'[ {message} ]: ')
	return temp

def add_food() -> None:

	header('Adding New Food')
	name = get_value('Enter Name')
	calories = get_int('Enter Calories')
	protein = get_int('Enter Protein')
	fat = get_int('Enter Fat')
	carb = get_int('Enter Carbs')

	food = Food(name,calories,protein,fat,carb)
	today.append(food)

def visulise_progress() -> None:

	header('Visualise Statistic')
	# sum of the subtance
	calories_sum = sum(food.calories for food in today)
	protein_sum = sum(food.protein for food in today)
	fat_sum = sum(food.fat for food in today)
	carbs_sum = sum(food.carbs for food in today)

	fig,axs = plt.subplots(2,2)
	axs[0,0].pie([protein_sum,fat_sum,carbs_sum],labels=['proteins','fats','carbs'],autopct='%1.1f%%')
	axs[0,0].set_title('Nutrients Distributions')

	axs[0,1].bar([0,1,2],[protein_sum,fat_sum,carbs_sum],width=0.4)
	axs[0,1].bar([0.5,1.5,2.5],[PROTEIN_GOAL,FAT_GOAL,CARBS_GOAL],width=0.4)
	axs[0,1].set_title('Nutrients Goal Progress')

	axs[1,0].pie([calories_sum,CALORIE_GOAL_LIMIT - calories_sum],labels=['calories','remaining'],autopct='%1.1f%%')
	axs[1,0].set_title('Calories Goal Remaining')

	axs[1,1].plot(list(range(len(today))),np.cumsum([food.calories for food in today]),label='Calories Consumption')
	axs[1,1].plot(list(range(len(today))),[CALORIE_GOAL_LIMIT] * len(today),label='Calories Goal')
	axs[1,1].legend()
	axs[1,1].set_title('Calorie Goal Progress')

	fig.tight_layout()
	plt.show()

def edit_goals() -> bool:
		header('Editing Goals')
		CALORIE_GOAL_LIMIT = get_int('Enter Calorie Goal Limit')
		FAT_GOAL = get_int('Enter Fat Goal')
		PROTEIN_GOAL = get_int('Enter Protein Goal')
		CARBS_GOAL = get_int('Enter Carbs Goal:')


def save_list() -> None:

	food_list:list[dict] = []

	for food in today:
		food_list.append({
							'name':food.name,
							'calories':food.calories,
							'protein':food.protein,
							'fat':food.fat,
							'carbs':food.carbs
						})

	mylist: dict = {
					'calories_goal_limit':CALORIE_GOAL_LIMIT,
					'protein_goal':PROTEIN_GOAL,
					'fat_goal':FAT_GOAL,
					'carbs_goal':CARBS_GOAL,
					'food_list':food_list
					}

	header('Saving List')
	filename = get_value('Enter Filename')

	with open(f'{filename}.json','w') as file:
		json.dump(mylist,file,indent=4)

def show_food_list() -> None:
	header('Food List')
	for food in today:
		print(f'Name: {food.name}')
		print(f'-> Calories: {food.calories}')
		print(f'-> Protein: {food.protein}')
		print(f'-> Fat: {food.fat}')
		print(f'-> Carbs: {food.carbs}')
		border()

	print(f'Total Calories:{sum(food.calories for food in today)}')
	print(f'Total Protein:{sum(food.protein for food in today)}')
	print(f'Total Fat:{sum(food.fat for food in today)}')
	print(f'Total Carbs:{sum(food.carbs for food in today)}')

def get_save_list() -> None:
	mylist:dict = {}
	header('Setting Save List')
	filename = get_value('Enter Filename')

	with open(f'{filename}.json','r') as file:
		mylist = json.load(file)

	CALORIE_GOAL_LIMIT = mylist['calories_goal_limit']
	FAT_GOAL = mylist['fat_goal']
	PROTEIN_GOAL = mylist['protein_goal']
	CARBS_GOAL = mylist['carbs_goal']
	for food in mylist['food_list']:
		today.append(Food(
							name = food['name'],
							calories = int(food['calories']),
							protein = int(food['protein']),
							fat = int(food['fat']),
							carbs = int(food['carbs'])
						 )
					)


def main() -> None:

	border()
	print('''
Terminal Calorie Tracker with Visualisation for Statistic Progress
Author: John Jayson B. De Leon
Github: savjaylade84
Email: savjaylade84@gmail.com
		''')

	is_done = False
	while not is_done:

		header('Command Option')
		print("""
(1) Add New Food
(2) Visualise Progress
(3) Edit Goals
(4) View Food List
(5) Save List
(6) Set Save List
(7) quit
			""")

		choice = get_value("Enter")

		if choice == '1':
			add_food()

		elif choice == '2':
			visulise_progress()

		elif choice == '3':
			edit_goals()

		elif choice == '4':
			show_food_list()

		elif choice == '5':
			save_list()

		elif choice == '6':
			get_save_list()

		elif choice == '7':
			is_done = not is_done
			header('Status: Exiting The Program')

		else:
			header('Status: Invalid Input')


if __name__ == '__main__':
	main()