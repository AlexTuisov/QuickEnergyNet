from src.market import simulate_market, plot_statistics
from src.iso import ISO
from src.controlled_producer import ControlledProducer
from src.market_agents.market_agent import MarketAgent
from src.market_agents.PCSUnit import PCSUnit
from src.demand_distribution import draw_demand

if __name__ == "__main__":

    # Number of timestamps for simulation
    num_timestamps = 48

    # Initialize ISO
    iso = ISO()


    # Example production price functions
    def linear_price(production_level):
        return 30 + 0.1 * production_level  # Base price of 30, increasing by 0.1 per unit


    def tiered_price(production_level):
        if production_level <= 200:
            return 25  # Flat rate for low production levels
        elif production_level <= 400:
            return 35  # Higher rate for mid-level production
        else:
            return 50  # Highest rate for high production levels


    # Initialize controlled producers
    controlled_producers = [
        ControlledProducer("Producer1", 500, linear_price),
        ControlledProducer("Producer2", 600, tiered_price)
    ]

    # Initialize market agents (using PCSUnit for flexibility)
    market_agents = [
        PCSUnit(
            agent_id=f"PCS_{i}",
            max_production=[60] * num_timestamps,  # Example production capacity
            internal_demand=[50] * num_timestamps,    # Example internal demand
            storage_capacity=500,                # Storage capacity
            initial_storage=0,                 # Initial storage
            production_price=70                  # Production price
        )
        for i in range(5)
    ]



    # Simulate the market
    stats = simulate_market(num_timestamps, iso, controlled_producers, market_agents)

    # Plot statistics
    plot_statistics(stats)
