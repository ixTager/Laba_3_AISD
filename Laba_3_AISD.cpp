#include <iostream>
#include <string>
#include <algorithm>

#include "TreeNode.h"
#include "TreeParser.h"
#include "AVLTree.h"

using namespace std;

template<typename T>
int getBinaryHeight(TreeNode<T>* node) {
    if (!node) return 0;

    return 1 + max(getBinaryHeight(node->left), getBinaryHeight(node->right));
}

template<typename T>
void bfs(AVLNode<T>* root) {
    if (!root) {
        cout << endl;
        return;
    }

    AVLNode<T>** queue = new AVLNode<T>*[100000];
    int front = 0;
    int rear = 0;

    queue[rear++] = root;

    bool first = true;

    while (front < rear) {
        AVLNode<T>* node = queue[front++];

        if (!first) cout << ", ";
        cout << node->value;
        first = false;

        if (node->left) queue[rear++] = node->left;
        if (node->right) queue[rear++] = node->right;
    }

    delete[] queue;
    cout << endl;
}

template<typename T>
void printPreorder(AVLNode<T>* node, bool& first) {
    if (!node) return;

    if (!first) cout << ", ";
    cout << node->value;
    first = false;

    printPreorder(node->left, first);
    printPreorder(node->right, first);
}

template<typename T>
void printInorder(AVLNode<T>* node, bool& first) {
    if (!node) return;

    printInorder(node->left, first);

    if (!first) cout << ", ";
    cout << node->value;
    first = false;

    printInorder(node->right, first);
}

template<typename T>
void printPostorder(AVLNode<T>* node, bool& first) {
    if (!node) return;

    printPostorder(node->left, first);
    printPostorder(node->right, first);

    if (!first) cout << ", ";
    cout << node->value;
    first = false;
}

template<typename T>
void clearBinaryTree(TreeNode<T>* node) {
    if (!node) return;

    clearBinaryTree(node->left);
    clearBinaryTree(node->right);

    delete node;
}

int main() {
    string input;

    if (!getline(cin, input)) {
        return 0;
    }

    TreeNode<int>* originalRoot = nullptr;

    try {
        TreeParser<int> parser(input);
        originalRoot = parser.parse();

        int originalHeight = getBinaryHeight(originalRoot);

        AVLTree<int> avl;
        avl.build(originalRoot);

        cout << input << "\n\n";

        cout << originalHeight << "\n";
        cout << avl.height() << "\n";

        bfs(avl.getRoot());

        bool first = true;
        printPreorder(avl.getRoot(), first);
        cout << "\n";

        first = true;
        printInorder(avl.getRoot(), first);
        cout << "\n";

        first = true;
        printPostorder(avl.getRoot(), first);
        cout << "\n";

        clearBinaryTree(originalRoot);
    }
    catch (exception& e) {
        clearBinaryTree(originalRoot);
        cerr << e.what() << endl;
        return 1;
    }

    return 0;
}
