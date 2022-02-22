const AnchorEarnPackage = require('@anchor-protocol/anchor-earn'); //import Anchor Earn
const Account = AnchorEarnPackage.Account
const AnchorEarn = AnchorEarnPackage.AnchorEarn;
const CHAINS = AnchorEarnPackage.CHAINS;
const DENOMS = AnchorEarnPackage.DENOMS;
const NETWORKS = AnchorEarnPackage.NETWORKS;



const getAnchorInfo = async (terra_address) => {
    try {
        const anchorEarn = new AnchorEarn({
            chain: CHAINS.TERRA,
            network: NETWORKS.COLUMBUS_5,
            address: terra_address
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
    const account = new Account(CHAINS.TERRA);
    addr = account.accAddress;
    let s = await getAnchorInfo(addr)
    console.log(JSON.stringify(s, null, 2))
})()