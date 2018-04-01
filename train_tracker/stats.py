################################################################################
#
# STATS
#
################################################################################

def stats(delays,config):
    
    # Function to calculate refund amount 
    def refund_calculator(delay):
        ticket_price = 500.80
        journey_price = ticket_price/40
        if 14 < delay < 30:
            refund = journey_price * 0.25
        if 29 < delay < 60:
            refund = journey_price * 0.5
        if delay > 60:
            refund = journey_price
        return refund

    refund_sum = delays["delay"].apply(refund_calculator).sum()
    num_delays = len(delays)
    print "You can claim: ", refund_sum, " from ", num_delays, " delayed trains"