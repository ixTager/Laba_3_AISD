#include "TreeNode.h"
#include "TreeParser.h"
#include "AVLTree.h"

#include <iostream>
#include <string>
#include <algorithm>
#include <exception>


template<typename T>
int getBinaryHeight(TreeNode<T>* node) {
    if (!node) return 0;

    return 1 + std::max(getBinaryHeight(node->left), getBinaryHeight(node->right));
}

template<typename T>
void clearBinaryTree(TreeNode<T>* node) {
    if (!node) return;

    clearBinaryTree(node->left);
    clearBinaryTree(node->right);

    delete node;
}

int main() {
    std::string input;

    if (!std::getline(std::cin, input)) {
        return 0;
    }

    TreeNode<int>* root = nullptr;

    try {
        TreeParser<int> parser(input);
        root = parser.parse();

        int inititalHeight = getBinaryHeight(root);

        AVLTree<int> avl;
        avl.build(root);

        std::cout << input << "\n\n";

        std::cout << inititalHeight << '\n';
        std::cout << avl.height() << '\n';

        avl.printBFS();

        avl.printDFSPreorder();
        avl.printDFSInorder();
        avl.printDFSPostorder();

        clearBinaryTree(root);
        root = nullptr;
    }
    catch (std::exception& e) {
        clearBinaryTree(root);

        std::cerr << e.what() << '\n';

        return 1;
    }

    return 0;
}
