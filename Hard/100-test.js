// Topics: Trees, Binary Search Tree, Recursion
// Problem: 98. Validate Binary Search Tree
// Difficulty: Medium

/**
 * Definition for a binary tree node.
 */
function TreeNode(val, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
}

/**
 * Validate if a binary tree is a Binary Search Tree (BST)
 * @param {TreeNode} root
 * @return {boolean}
 */
var isValidBST = function(root) {
    /**
     * Helper function to validate subtree
     * @param {TreeNode} node - Current node
     * @param {number} low - Lower bound (exclusive)
     * @param {number} high - Upper bound (exclusive)
     * @return {boolean}
     */
    const validate = (node, low = -Infinity, high = Infinity) => {
        if (!node) return true;
        if (node.val <= low || node.val >= high) return false;
        return validate(node.left, low, node.val) && 
               validate(node.right, node.val, high);
    };
    
    return validate(root);
};

// Time Complexity: O(n) - visit each node once
// Space Complexity: O(h) - h is height, recursion stack
