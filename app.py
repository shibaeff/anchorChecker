from anchorearn import Account, AnchorEarn

async def getAnchorInfo(terraAddress):
    try:
          anchorEarn = AnchorEarn(chain=CHAINS.TERRA, network=NETWORKS.COLUMBUS_5, address=terraAddress)
    except:
        pass
