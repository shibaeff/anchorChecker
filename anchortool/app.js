const AnchorEarnPackage = require('@anchor-protocol/anchor-earn'); //import Anchor Earn
const Account = AnchorEarnPackage.Account
const AnchorEarn = AnchorEarnPackage.AnchorEarn;
const CHAINS = AnchorEarnPackage.CHAINS;
const DENOMS = AnchorEarnPackage.DENOMS;
const NETWORKS = AnchorEarnPackage.NETWORKS;

const account = new Account(CHAINS.TERRA);

const getAnchorInfo = async (terra_address, res, next) => {
    try {
        const anchorEarn = new AnchorEarn({
            chain: CHAINS.TERRA,
            network: NETWORKS.COLUMBUS_5,
            address: terra_address
        });

        const userBalance = await anchorEarn.balance({
            currencies: [DENOMS.UST],
        });

        const marketInfo = await anchorEarn.market({
            currencies: [
                DENOMS.UST
            ],
        });

        return {
            // Current_Balance: userBalance.balances[0].deposit_balance,
            APY: marketInfo.markets[0].APY * 100,
            Timestamp: marketInfo.timestamp
        };
    }
    catch (exception) {
        console.error("Exception thrown", exception.stack);
        return { "message": "Error Occured!" };
    }

};

(async () => {
    console.log((await getAnchorInfo(account.accAddress)))
})()