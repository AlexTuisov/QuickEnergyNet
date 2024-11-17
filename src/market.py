from src.controlled_producer import ControlledProducer
from src.iso import ISO
from src.market_agents.market_agent import MarketAgent
from src.demand_distribution import draw_demand


def simulate_market(num_timestamps, iso, controlled_producers, market_agents):
    """
    Simulates the market over a given number of timestamps.

    Args:
        num_timestamps (int): Number of timestamps to simulate.
        iso (ISO): Initialized ISO instance.
        controlled_producers (list): List of initialized ControlledProducer instances.
        market_agents (list): List of initialized MarketAgent instances.

    Returns:
        list: Statistics collected during the simulation.
    """
    # Statistics storage
    statistics = []

    for t in range(num_timestamps):
        print(f"\n--- Timestamp {t} ---")

        # Step 1: Draw demand
        demand = draw_demand(t, demand_type="sinusoidal")
        print(f"Demand: {demand}")

        # Step 2: ISO decides actions
        iso_action = iso.decide_action(t, demand, controlled_producers, market_agents)
        production_orders = iso_action["production_orders"]
        agent_prices = iso_action["agent_prices"]

        # Assign production orders to controlled producers
        for producer, order in zip(controlled_producers, production_orders):
            producer.production_order = order

        # Print production orders and market prices
        print(f"ISO Production Orders: {production_orders}")
        for i, price in enumerate(agent_prices):
            print(f"Market Agent {i} Prices: Buy @ {price['buy_price']}, Sell @ {price['sell_price']}")
        print(iso_action)
        # Step 3: Market agents create orders
        total_agent_buy = 0
        total_agent_sell = 0
        for agent, prices in zip(market_agents, iso_action["agent_prices"]):
            # Use individual prices for each agent
            order = agent.create_order(t, prices["buy_price"], prices["sell_price"])
            print(f"{agent.agent_id} Order: {order}")
            total_agent_buy += order["buy_amount"]
            total_agent_sell += order["sell_amount"]

        # Step 4: Calculate totals and gather statistics
        total_controlled_production = sum(producer.production_order for producer in controlled_producers)
        net_demand = demand - total_controlled_production - (total_agent_buy - total_agent_sell)

        # Calculate the cost of controlled production
        controlled_production_cost = sum(
            producer.production_order * producer.get_production_cost(producer.production_order)
            for producer in controlled_producers
        )

        # Calculate the cost of transactions with market agents
        market_transaction_cost = sum(
            agent.create_order(t, prices["buy_price"], prices["sell_price"])["buy_amount"] * prices["sell_price"]
            - agent.create_order(t, prices["buy_price"], prices["sell_price"])["sell_amount"] * prices["buy_price"]
            for agent, prices in zip(market_agents, iso_action["agent_prices"])
        )

        # Total cost to ISO
        total_cost = controlled_production_cost + market_transaction_cost

        stats = {
            'timestamp': t,
            'demand': demand,
            'controlled_production': total_controlled_production,
            'total_agent_buy': total_agent_buy,
            'total_agent_sell': total_agent_sell,
            'net_demand': net_demand,
            'total_cost': total_cost
        }
        statistics.append(stats)

        # Output the statistics for this timestamp
        print(f"Total Controlled Production: {total_controlled_production}")
        print(f"Total Agent Buy: {total_agent_buy}")
        print(f"Total Agent Sell: {total_agent_sell}")
        print(f"Net Demand: {net_demand}")
        print(f"Total Cost to ISO: {total_cost}")

    return statistics


def plot_statistics(stats):
    import matplotlib.pyplot as plt
    import numpy as np

    # Extract data
    timestamps = [s['timestamp'] for s in stats]
    demands = [s['demand'] for s in stats]
    controlled_productions = [s['controlled_production'] for s in stats]
    total_agent_buys = [s['total_agent_buy'] for s in stats]
    total_agent_sells = [s['total_agent_sell'] for s in stats]

    # Adjust the demand based on market agents' behavior
    adjusted_demands = [
        demand + max(0, total_agent_buy - total_agent_sell)  # Add only if agents are buying on aggregate
        for demand, total_agent_buy, total_agent_sell in zip(demands, total_agent_buys, total_agent_sells)
    ]

    # Calculate the bar components
    agent_contributions = [
        max(0, total_agent_sell - total_agent_buy)  # Agents contribute only if selling more than buying
        for total_agent_buy, total_agent_sell in zip(total_agent_buys, total_agent_sells)
    ]
    unmet_demands = [
        max(0, adjusted_demand - controlled - agent)  # Remaining unmet demand
        for adjusted_demand, controlled, agent in zip(adjusted_demands, controlled_productions, agent_contributions)
    ]

    # Plot the stacked bar chart
    bar_width = 0.8
    x_indices = np.arange(len(timestamps))

    plt.figure(figsize=(12, 8))

    # Controlled producer output
    plt.bar(x_indices, controlled_productions, color='lightblue', label='Controlled Producers', width=bar_width)
    # Market agent contributions (only appears if agents are selling more on aggregate)
    plt.bar(x_indices, agent_contributions, bottom=controlled_productions, color='lightgreen', label='Market Agents', width=bar_width)
    # Unmet demand
    plt.bar(
        x_indices,
        unmet_demands,
        bottom=[c + a for c, a in zip(controlled_productions, agent_contributions)],
        color='yellow',
        label='Unmet Demand',
        width=bar_width,
    )

    # Add the original demand as a black line with dots
    plt.plot(x_indices, demands, color='black', marker='o', label='Original Demand', linewidth=2)

    # Configure chart
    plt.title('Demand and Supply Breakdown Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Electricity (MW)')
    plt.xticks(x_indices, timestamps)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()





