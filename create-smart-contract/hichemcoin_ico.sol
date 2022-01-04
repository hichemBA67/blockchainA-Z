pragma solidity ^0.4.11;

contract hichemcoin_ico {

    // Introducing the maxiumum number of Hichemcoins available for sale
    uint public max_hichemcoins = 1000000;

    // Introducing the USD to Hichemcoin conversion rate
    uint public usd_to_hichemcoins = 1000;

    // Introducing the total number of Hichemcoins bought by the investors
    uint public total_hichemcoins_bought;

    // Mapping from the investor address to its equity in Hichemcoins and USD
    mapping(address => uint) equity_hichemcoins;
    mapping(address => uint) equity_usd;

    // Check if investor can buy Hichemcoin
    modifier canBuyHichemcoins(uint _usd_invested) {
        require(_usd_invested * usd_to_hichemcoins + total_hichemcoins_bought <= max_hichemcoins, "The entered amount exceeds the available amount of Hichemcoins");
        _;
    }

    // Getting the equity in Hichemcoins of investor
    function get_equity_in_hichemcoin(address _investor) external view returns(uint) {
        return equity_hichemcoins[_investor];
    }
    // Getting the equity in USD of investor
    function get_equity_in_usd(address _investor) external view returns(uint) {
        return equity_usd[_investor];
    }

    // Buying Hichemcoin
    function buy_hichemcoins(address _investor, uint _usd_invested) external canBuyHichemcoins(_usd_invested){
        uint hadcoins_bought = _usd_invested * usd_to_hichemcoins;
        equity_hichemcoins[_investor] += hadcoins_bought;
        equity_usd[_investor] = equity_hichemcoins[_investor] / usd_to_hichemcoins;
        total_hichemcoins_bought += hadcoins_bought;
    }

    // Sell Hichemcoin
    function sell_hichemcoin(address _investor, uint hichemcoins_sold) external {
        equity_hichemcoins[_investor] -= hichemcoins_sold;
        equity_usd[_investor] = equity_hichemcoins[_investor] / usd_to_hichemcoins;
        total_hichemcoins_bought -= hichemcoins_sold;
    }
}