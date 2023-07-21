import streamlit as st
import yaml


class Backtester:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.scenarios = []

    def add_scenario(self, scenario):
        self.scenarios.append(scenario)

    def run(self):
        for scenario in self.scenarios:
            scenario.apply(self.portfolio)

    def get_results(self):
        return self.portfolio


class Scenario:
    def __init__(self, name, description, effect, parameters):
        self.name = name
        self.description = description
        self.effect = effect
        self.parameters = parameters


# Load scenarios from YAML config files
with open("scenarios.yaml", "r") as file:
    scenarios = yaml.safe_load(file)

# Initialize scenario objects
scenario_objects = [Scenario(**scenario) for scenario in scenarios]

# Streamlit interface
st.title("Backtester 3000 Game")

# Game introduction and instructions
st.write(
    """
Welcome to the Backtester 3000 Game! In this game, you'll manage a virtual investment portfolio and see how it performs under a variety of wild and unpredictable scenarios. The goal of the game is to end up with as much money as possible. Good luck!
"""
)

# Set up the initial portfolio
st.header("Set Up Your Portfolio")
stocks = st.text_input(
    "Enter the stocks in your portfolio, separated by commas (e.g., 'SNOW, CRM, MSFT')",
    key="stocks_input",
).split(",")
amounts = st.text_input(
    "Enter the corresponding amounts of each stock in your portfolio, separated by commas (e.g., '100, 200, 300')",
    key="amounts_input",
).split(",")
portfolio = dict(zip(stocks, amounts))

# Tinder-like feature to choose scenarios
st.header("Choose Your Scenarios")
st.write(
    """
Now, you'll choose the scenarios you want to simulate. Swipe right if you want to include a scenario in your simulation, or swipe left if you don't.
"""
)
# Use session state to remember the current scenario and the user's selections
if "scenario_index" not in st.session_state:
    st.session_state.scenario_index = 0
if "selected_scenarios" not in st.session_state:
    st.session_state.selected_scenarios = []

# Display the current scenario
st.write(f"Current scenario: {scenario_objects[st.session_state.scenario_index].name}")

# Create the columns
columns = st.columns(4)

# Add a button to each column
if columns[0].button("Like"):
    # Add the current scenario to the selected scenarios
    st.session_state.selected_scenarios.append(
        scenario_objects[st.session_state.scenario_index].name
    )
if columns[1].button("Pass"):
    # Do nothing (the user doesn't like the current scenario)
    pass
if columns[2].button("Previous"):
    # Go back to the previous scenario
    st.session_state.scenario_index = max(0, st.session_state.scenario_index - 1)
if columns[3].button("Next"):
    # Go to the next scenario
    st.session_state.scenario_index = min(
        len(scenario_objects) - 1, st.session_state.scenario_index + 1
    )


# Run the backtest when the user clicks the button
if st.button("Start Game"):
    backtester = Backtester(portfolio)
    for scenario_name in st.session_state.selected_scenarios:
        scenario = next(
            scenario for scenario in scenario_objects if scenario.name == scenario_name
        )
        backtester.add_scenario(scenario)
    backtester.run()
    results = backtester.get_results()

    # Display the results
    st.subheader("Results")
    st.line_chart(results)
    st.write(f"You ended up with ${sum(results.values())}!")
