#pragma once

#include "TreeNode.h"
#include <string>
#include <stdexcept>
#include <cctype>

template<typename T>
class TreeParser {
private:
    const std::string& expression;
    int position = 0;

    void skipSpaces() {
        while (position < expression.size() &&
            std::isspace(static_cast<unsigned char>(expression[position]))) {
            position++;
        }
    }

    T readValue() {
        skipSpaces();

        int start = position;

        if (position < expression.size() && (expression[position] == '-' || expression[position] == '+')) {
            position++;
        }

        while (position < expression.size() && std::isdigit(static_cast<unsigned char>(expression[position]))) {
            position++;
        }

        if (start == position || (position == start + 1 && (expression[start] == '-' || expression[start] == '+'))) {
            throw std::runtime_error("Invalid node value");
        }

        return static_cast<T>(std::stoi(expression.substr(start, position - start)));
    }

    TreeNode<T>* parseNode() {
        skipSpaces();

        if (position >= expression.size() || expression[position] != '(') {
            throw std::runtime_error("Expected '('");
        }

        position++;

        T value = readValue();

        TreeNode<T>* node = new TreeNode<T>(value);

        try {
            skipSpaces();

            if (position < expression.size() && expression[position] == '(') {
                node->left = parseNode();
            }

            skipSpaces();

            if (position < expression.size() && expression[position] == '(') {
                node->right = parseNode();
            }

            skipSpaces();

            if (position >= expression.size() || expression[position] != ')') {
                throw std::runtime_error("Expected ')'");
            }

            position++;

            return node;
        }
        catch (...) {
            clear(node);
            throw;
        }
    }

    void clear(TreeNode<T>* node) {
        if (node == nullptr) return;

        clear(node->left);
        clear(node->right);

        delete node;
    }

public:
    TreeParser(std::string& input): expression(input) { }

    TreeNode<T>* parse() {
        TreeNode<T>* root = parseNode();

        skipSpaces();

        if (position != expression.size()) {
            clear(root);
            throw std::runtime_error("Unexpected characters");
        }

        return root;
    }
};
