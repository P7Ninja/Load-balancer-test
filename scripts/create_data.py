import bcrypt
from faker import Faker
import random
import sys
import argparse
import tqdm
from datetime import datetime
fake = Faker()
recipe_names = [
        "Pancakes",
        "Hamburger",
        "Spaghetti",
        "Pizza",
        "Lasagna",
        "Pasta",
        "Pasta Salad",
        "Chicken",
        "Chicken Salad",
        "Chicken Soup",
        "Chicken Noodle Soup",
        "Chicken and Rice",
        "Chicken and Dumplings",
        "English breakfast",
        "French toast",
        "Eggs Benedict",
        "Omelette",
        "Waffles",
    ]
units = ["g", "ml", "l"]
items = [ "tomato",  "chicken", "beef", "pork", "potato", "rice", "pasta", "noodles", "cheese", "milk" ]
tags = ["Morgenmad", "Middagsmad", "Aftensmad"]


def create_users(amount: int):
    user_fmt = "('{username}','{password}','{email}','{gender}','{birthday}',{calories},{fat},{carbohydrates},{protein}){last} /*{unhashed_password}*/"
    users = []

    admin = user_fmt.format(
            username="admin",
            password=bcrypt.hashpw("admin".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            unhashed_password="admin",
            email=fake.email(),
            gender="male",
            birthday=fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%Y-%m-%d"),
            calories=random.randint(1000, 3000),
            fat=random.randint(0, 100),
            carbohydrates=random.randint(0, 100),
            protein=random.randint(0, 100),
            last=";" if amount == 0 else ","
        )
    users.append(admin)
    for i in tqdm.tqdm(range(amount), desc="Creating users"):
        password = fake.password(special_chars=False)
        gender = random.choice(["male", "female"])
        user = user_fmt.format(
            username=fake.user_name(),
            password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            unhashed_password=password,
            email=fake.email(),
            gender=gender,
            birthday=fake.date_of_birth(minimum_age=18, maximum_age=60).strftime("%Y-%m-%d"),
            calories=random.randint(1000, 3000),
            fat=random.randint(0, 100),
            carbohydrates=random.randint(0, 100),
            protein=random.randint(0, 100),
            last=";" if i == amount - 1 else ","
        )
        users.append(user)
    return "INSERT INTO users (username, password, email, gender, birthday, calories, fat, carbohydrates, protein) VALUES\n" + "\n".join(users)

def create_recipes(amount: int):
    recipe_fmt = "('{title}', {servings}, '{instructions}', '{url}'){last}"
    unit_fmt = "('{name}'){last}"
    item_fmt = "('{name}'){last}"
    energy_fmt = "({calories}, {fat}, {protein}, {carbohydrates}, {recipe_id}){last}"
    ingredient_fmt = "({amount}, {unit_id}, {item_id}, {recipe_id}){last}"
    tag_fmt = "('{tag}'){last}"
    tag_recipe_fmt = "({recipe_id}, {tag_id}){last}"
    # list of recipe names
    used_names: dict[str, int] = dict()
    sql_recipes = []
    sql_units = []
    sql_items = []
    sql_energy = []
    sql_ingredients = []
    sql_tags = []
    sql_tag_recipes = []

    for i in range(amount):
        title = random.choice(recipe_names)
        if title in used_names:
            used_names[title] += 1
            title += str(used_names[title])
        else:
            used_names[title] = 1
        recipe = recipe_fmt.format(
            title=title,
            servings=random.randint(1, 10),
            instructions=fake.paragraph(nb_sentences=5),
            url=fake.url(),
            last=";" if i == amount - 1 else ","
        )
        sql_recipes.append(recipe)
    
    
    for unit in units:
        sql_units.append(unit_fmt.format(name=unit, last=";" if unit == units[-1] else ","))
        
    for item in items:
        sql_items.append(item_fmt.format(name=item, last=";" if item == items[-1] else ","))
    
    for tag in tags:
        sql_tags.append(tag_fmt.format(tag=tag, last=";" if tag == tags[-1] else ","))

    
    for i in tqdm.tqdm(range(amount), desc="Creating recipes"):
        recipe_id = i + 1
        used_items = set()
        sql_energy.append(energy_fmt.format(
            calories=random.randint(100, 1000),
            fat=random.randint(0, 100),
            protein=random.randint(0, 100),
            carbohydrates=random.randint(0, 100),
            recipe_id=recipe_id,
            last=";" if i == amount - 1 else ","
        ))
        ingredient_count = random.randint(1, 10)
        for j in range(ingredient_count):
            item_id = random.randint(1, len(items))
            while item_id in used_items:
                item_id = random.randint(1, len(items))
            sql_ingredients.append(ingredient_fmt.format(
                amount=random.randint(1, 500),
                unit_id=random.randint(1, len(units)),
                item_id=item_id,
                recipe_id=recipe_id,
                last=";" if i == amount - 1 and j == ingredient_count - 1 else ","
            ))
            used_items.add(item_id)

        tag = random.randint(1, len(tags))
        sql_tag_recipes.append(tag_recipe_fmt.format(
            tag_id=tag,
            recipe_id=recipe_id,
            last=";" if i == amount - 1 else ","
        ))

    insert_recipes = "INSERT INTO recipes (title, servings, instructions, url) VALUES\n" + "\n".join(sql_recipes)
    insert_units = "INSERT INTO units (name) VALUES\n" + "\n".join(sql_units)
    insert_items = "INSERT INTO items (name) VALUES\n" + "\n".join(sql_items)
    insert_energy = "INSERT INTO energy (calories, fat, protein, carbohydrates, recipe_id) VALUES\n" + "\n".join(sql_energy)
    insert_ingredients = "INSERT INTO ingredients (amount, unit_id, item_id, recipe_id) VALUES\n" + "\n".join(sql_ingredients)
    insert_tags = "INSERT INTO tags (tag) VALUES\n" + "\n".join(sql_tags)
    insert_recipe_tag_association = "INSERT INTO recipe_tag_association (recipe_id, tag_id) VALUES\n" + "\n".join(sql_tag_recipes)
    return "\n".join([insert_recipes, insert_units, insert_items, insert_energy, insert_ingredients, insert_tags, insert_recipe_tag_association])

def create_health_log(user_count: int, max_amount: int):
    health_fmt = "({user_id}, '{dateStamp}', {height}, {weight}, {fatPercentage}, {musclePercentage}, {waterPercentage}){last}"
    healths = []
    for user_id in tqdm.tqdm(range(1, user_count + 2), desc="Creating health logs"):
        health_count = random.randint(0, max_amount)
        for i in range(health_count):
            fat = random.randint(3, 40)
            muscle = random.randint(33, 60)
            water = 100 - fat - muscle
            health = health_fmt.format(
                user_id=user_id,
                dateStamp=fake.date_time().strftime("%Y-%m-%d %H:%M:%S"),
                height=random.randint(150, 220),
                weight=random.randint(50, 150),
                fatPercentage=fat,
                musclePercentage=muscle,
                waterPercentage=water,
                last=";" if i == health_count - 1 and user_id == user_count + 1  else ","
            )
            healths.append(health)
    return "INSERT INTO healthLog (userID, dateStamp, height, weight, fatPercentage, musclePercentage, waterPercentage) VALUES\n" + "\n".join(healths)
            
def create_food():
    food_fmt = "('{name}', {price}, {priceKg}, {discount}, '{vendor}', {category},  {cal}, {fat}, {carbs}, {protein}){last}"
    foods = []
    for i in tqdm.tqdm(range(len(items)), desc="Creating food"):
        food = food_fmt.format(
            name=items[i],
            price=random.randint(1, 100),
            priceKg=random.randint(1, 100),
            discount=random.randint(0, 100),
            vendor=fake.word(),
            category=random.randint(0, 100),
            cal=random.randint(1, 100),
            fat=random.randint(1, 100),
            carbs=random.randint(1, 100),
            protein=random.randint(1, 100),
            last=";" if i == len(items) - 1 else ","
        )
        foods.append(food)
    return "INSERT INTO Foods (Name, Price, PriceKg, Discount, Vendor, Category, Cal, Fat, Carbs, Protein) VALUES\n" + "\n".join(foods)

def create_inventory(user_count: int, max_amount: int):
    inventory_fmt = "({user_id}, '{name}'){last}"
    inventory_items_fmt = "({inventory_id}, {food_id}, '{expiration_date}'){last}"

    inventories = []
    inventory_items = []
    for user_id in tqdm.tqdm(range(1, user_count + 2), desc="Creating inventories"):
        inventory = inventory_fmt.format(
            user_id=user_id,
            name=fake.word(),
            last=";" if user_id == user_count + 1 else ","
        )

        inventories.append(inventory)
        amount = random.randint(0, max_amount)
        for j in range(amount):
            inventory_items.append(inventory_items_fmt.format(
            inventory_id=user_id,
            food_id=random.randint(1, len(items)),
            expiration_date=fake.date_time_ad(start_datetime=datetime(2023, 1, 1)).strftime("%Y-%m-%d %H:%M:%S"),
            last=";" if j == amount - 1 and user_id == user_count + 1 else ","
            ))
    inventories_sql = "INSERT INTO Inventories (UserId, Name) VALUES\n" + "\n".join(inventories)
    inventory_items_sql = "INSERT INTO InventoryItems (InventoryID, FoodID, ExpirationDate) VALUES\n" + "\n".join(inventory_items)

    return "\n".join([inventories_sql, inventory_items_sql])
    
def create_mealplan(user_count: int, recipes_count: int):
    mealplan_fmt = "({userID}, '{startDate}', '{endDate}'){last}"
    mealsperday_fmt = "({planID}, {meals}, {totalCalories}, {totalProtein}, {totalCarbohydrates}, {totalFat}){last}"
    mealplanrecipes_fmt = "({planID}, {recipeID}){last}"

    mealplans = []
    mealsperday = []
    mealplanrecipes = []

    mealplan_id = 1
    startdate = fake.date_this_year().strftime("%Y-%m-%d")
    for user_id in tqdm.tqdm(range(1, user_count + 2), desc="Creating mealplans"):
        mealplan = mealplan_fmt.format(
            userID=user_id,
            startDate=startdate,
            endDate=startdate,
            last=";" if user_id == user_count + 1 else ","
        )
        mealplans.append(mealplan)
        mealsperday.append(mealsperday_fmt.format(
                planID=mealplan_id,
                meals=3,
                totalCalories=random.randint(1000, 3000),
                totalProtein=random.randint(0, 100),
                totalCarbohydrates=random.randint(0, 100),
                totalFat=random.randint(0, 100),
                last=";" if user_id == user_count + 1 else ","
            ))
        for i in range(3):
            mealplanrecipes.append(mealplanrecipes_fmt.format(
                planID=mealplan_id,
                recipeID=random.randint(1, recipes_count),
                last=";" if user_id == user_count + 1 and i == 2 else ","
            ))
        mealplan_id += 1
        
    
    mealplans_sql = "INSERT INTO mealplan (userID, startDate, endDate) VALUES\n" + "\n".join(mealplans)
    mealsperday_sql = "INSERT INTO mealsperday (planID, meals, totalCalories, totalProtein, totalCarbohydrates, totalFat) VALUES\n" + "\n".join(mealsperday)
    mealplanrecipes_sql = "INSERT INTO mealplanrecipes (planID, recipeID) VALUES\n" + "\n".join(mealplanrecipes)

    return "\n".join([mealplans_sql, mealsperday_sql, mealplanrecipes_sql])

def create_test_data(
        users_count: int, 
        recipe_count: int, 
        max_health_log: int, 
        max_inventory: int):
    users = create_users(users_count)
    recipes = create_recipes(recipe_count)
    healths = create_health_log(users_count, max_health_log)
    foods = create_food()
    inventory = create_inventory(users_count, max_inventory)
    mealplans = create_mealplan(users_count, recipe_count)

    return "\n".join([
        "use users;",
        users, 
        "use recipes;",
        recipes, 
        "use health;",
        healths, 
        "use food;",
        foods, 
        "use inventory;",
        inventory,
        "use mealplan;", 
        mealplans])
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create test data for the database")
    parser.add_argument("-u", "--users", type=int, help="Number of users to create", default=10)
    parser.add_argument("-r", "--recipes", type=int, help="Number of recipes to create", default=50)
    parser.add_argument("-l", "--health-log", type=int, help="Maximum number of health logs per user", default=10)
    parser.add_argument("-i", "--inventory", type=int, help="Maximum number of inventory items per user", default=10)
    parser.add_argument("-o", "--output", type=str, help="Output file", default=None)
    parser.add_argument("--seed", type=int, help="Seed for the random number generator", default=None)

    args = parser.parse_args()

    seed = random.randrange(sys.maxsize)
    if args.seed is not None:
        seed = args.seed
    
    random.seed(args.seed)

    data = create_test_data(args.users, args.recipes, args.health_log, args.inventory)
    
    if args.output is None:
        print(data)
    else:
        with open(args.output, "w") as f:
            f.write(data)
            f.write("\n -- Seed: " + str(seed))
    print(f"Seed: {seed}")