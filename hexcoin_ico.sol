//SPDX-License-Identifier: UNLICENSED
//Hexcoin ICO

pragma solidity >=0.7.0 <0.9.0;

contract hexcoin_ico{
    uint public max_hexcoins = 1000000;
    uint public rupee_to_hexcoin = 1000;
    uint public total_hexcoins_bought = 0;
    
    mapping(address => uint) equity_hexcoins;
    mapping(address => uint) equity_usd;

    modifier can_buy_hexcoin(uint usd_invested){
        require (usd_invested * rupee_to_hexcoin + total_hexcoins_bought <= max_hexcoins);
        _;
    }

    //getting the equity in hexcoins of an investor
    function equity_in_hexcoins(address investor) external view returns(uint){
        return equity_hexcoins[investor];
    }

    //getting the equity in usd of an investor
    function equity_in_usd(address investor) external view returns(uint){
        return equity_usd[investor];
    }

    //a function to buy hexcoins 
    function buy_hexcoins(address investor, uint amount_invested) external
    can_buy_hexcoin(amount_invested){
        uint new_hexcoins = amount_invested*rupee_to_hexcoin;
        equity_hexcoins[investor] += new_hexcoins;
        equity_usd[investor] = equity_hexcoins[investor]/rupee_to_hexcoin ;
        total_hexcoins_bought+=new_hexcoins;
    }

    //selling hexcoins <buyback>
    function sell_hexcoins(address investor,uint hexcoins_sold) external{
        equity_hexcoins[investor] -= hexcoins_sold;
        equity_usd[investor] = equity_hexcoins[investor]/rupee_to_hexcoin;
        total_hexcoins_bought -= hexcoins_sold;
    }
}

