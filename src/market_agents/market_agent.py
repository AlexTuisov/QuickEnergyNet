from abc import ABC, abstractmethod

class MarketAgent(ABC):
    def __init__(self, agent_id):
        """
        Abstract base class for market agents.

        Args:
            agent_id (str): Unique identifier for the agent.
        """
        self.agent_id = agent_id

    @abstractmethod
    def create_order(self, timestamp, buy_price, sell_price):
        """
        Abstract method to generate a buy/sell order.

        Args:
            timestamp (int): Current timestamp.
            buy_price (float): Price at which the ISO is buying electricity.
            sell_price (float): Price at which the ISO is selling electricity.

        Returns:
            dict: Order with `buy_amount` and `sell_amount`.
        """
        pass

