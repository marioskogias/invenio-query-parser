"""Implement an invenion query AST to elasticsearch dsl converter"""

from .. import ast
from ..visitor import make_visitor


class ASTtoDSLConverter(object):
    visitor = make_visitor()

    # not analyzed fields should be used as filters
    #NOT_ANALYZED_FIELDS = set(["baz","boo"])

    @visitor(ast.KeywordOp)
    def visit(self, node, keyword, value):
        """This function should return either a filter or a query
           For now on it returns only queries
        """
        return value(keyword.value)

    @visitor(ast.AndOp)
    def visit(self, node, left, right):
        return {"bool" : {"must": [left, right]}}

    @visitor(ast.OrOp)
    def visit(self, node, left, right):
        return {"bool" : {"should": [left, right]}}

    @visitor(ast.NotOp)
    def visit(self, node, child):
        return {"bool" : {"must_not": [child]}}

    @visitor(ast.ValueQuery)
    def visit(self, node, child):
        return child("_all")

    @visitor(ast.Keyword)
    def visit(self, node):
        return node

    @visitor(ast.Value)
    def visit(self, node):
        return lambda x : {"match": { str(x): str(node.value)}}

    @visitor(ast.SingleQuotedValue)
    def visit(self, node):
        return lambda x : {"match_phrase": { str(x): str(node.value)}}

    @visitor(ast.DoubleQuotedValue)
    def visit(self, node):
        return lambda x : {"match": { str(x): str(node.value)}}

    @visitor(ast.RangeOp)
    def visit(self, node, left, right):
        return lambda x : {"range": { str(x): {"gte": node.left.value, "lte": node.right.value}}}

