from flask import Flask, render_template
import pandas as pd

# Chart Preparation Functions


def labels(df):
    return [col for col in df['Set Name']]


def data(df):
    return [round(col, 2) for col in df['Market Price']]


# Part I Highest Average Price per set per card type
df_card_type_total = pd.read_csv("analysis/total/total_card_type_avg_price.csv")
df_energy = pd.read_csv("analysis/energy/energy_highest_avg_set_price.csv")[:5]
df_item = pd.read_csv("analysis/item/item_highest_avg_set_price.csv")[:5]
df_stadium = pd.read_csv("analysis/stadium/stadium_highest_avg_set_price.csv")[:5]
df_tool = pd.read_csv("analysis/tool/tool_highest_avg_set_price.csv")[:5]
df_supporter = pd.read_csv("analysis/supporter/supporter_highest_avg_set_price.csv")[:5]
df_pokemon = pd.read_csv("analysis/pokemon/pokemon_highest_avg_set_price.csv")[:5]

# Part II Top 10 of Pokemon count and Avg price per pokemon
df_pokemon_ct = pd.read_csv("analysis/pokemon/count_by_pokemon")[:10]
df_pokemon_price = pd.read_csv("analysis/pokemon/avg_price_per_pokemon")[:10]

# Part III Top 5 Average Price per set
df_set_avg_price = pd.read_csv("analysis/total/total_highest_avg_set_price.csv")[:5]

# Part IV Pop Series 5 Expected Value
df_pop = pd.read_csv("analysis/pokemon/pop_series.csv")
df_pop = df_pop.sort_values(by=['Market Price'], ascending=False)[:2]
expect_value = []
for value in df_pop['Market Price'].to_list():
    exp_val = round(value * (1/40), 2)
    expect_value.append(exp_val)

app = Flask(__name__)


@app.route('/')
def home():

    # Pokemon and total data and labels
    total_labels = [col for col in df_card_type_total['Card Type']]
    pokemon_ct_labels = [col for col in df_pokemon_ct['Pokemon Name']]
    pokemon_ct_data = [col for col in df_pokemon_ct['count']]
    pokemon_price_labels = [col for col in df_pokemon_price['Pokemon Name']]
    pokemon_price_data = data(df_pokemon_price)

    return render_template("index.html", energy_labels=labels(df_energy), energy_data=data(df_energy),
                           item_labels=labels(df_item), item_data=data(df_item), stadium_labels=labels(df_stadium),
                           stadium_data=data(df_stadium), tool_labels=labels(df_tool), tool_data=data(df_tool),
                           supporter_labels=labels(df_supporter), supporter_data=data(df_supporter),
                           pokemon_labels=labels(df_pokemon), pokemon_data=data(df_pokemon),
                           total_labels=total_labels, total_data=data(df_card_type_total),
                           pokemon_ct_labels=pokemon_ct_labels, pokemon_ct_data=pokemon_ct_data,
                           pokemon_price_labels=pokemon_price_labels, pokemon_price_data=pokemon_price_data,
                           set_rank_labels=labels(df_set_avg_price), set_rank_data=data(df_set_avg_price),
                           pop_5_name=df_pop['Card Name'].to_list(), pop_5_price=df_pop['Market Price'].to_list(),
                           pull_rate="1/40", exp_val=expect_value,
                           pt_one_len=5, pt_one_total=6, pt_two_len=10)


@app.route('/regression')
def regression():
    return render_template("pokemon-regression.nb.html")


if __name__ == "__main__":
    app.run()
