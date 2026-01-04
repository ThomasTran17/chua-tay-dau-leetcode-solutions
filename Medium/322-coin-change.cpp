// Topics: Dynamic Programming, Array, Backtracking
// Problem: 322. Coin Change
// Difficulty: Medium

#include <vector>
#include <algorithm>
#include <limits.h>
using namespace std;

class Solution {
public:
    /**
     * Return the fewest number of coins needed to make the amount.
     * Return -1 if amount cannot be made.
     * 
     * @param coins Vector of coin denominations
     * @param amount Target amount
     * @return Minimum number of coins needed, or -1 if impossible
     */
    int coinChange(vector<int>& coins, int amount) {
        // DP array: dp[i] = minimum coins needed for amount i
        vector<int> dp(amount + 1, INT_MAX);
        dp[0] = 0;  // Base case: 0 coins needed for amount 0
        
        // Build up solutions for amounts 1 to target amount
        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (coin <= i && dp[i - coin] != INT_MAX) {
                    dp[i] = min(dp[i], dp[i - coin] + 1);
                }
            }
        }
        
        return dp[amount] == INT_MAX ? -1 : dp[amount];
    }
};

// Time Complexity: O(amount * len(coins))
// Space Complexity: O(amount)
// Example: coins = [1,2,5], amount = 5
// Output: 2 (5 = 5 or 5 = 2+2+1)
