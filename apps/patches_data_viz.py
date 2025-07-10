import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import polars as pl
    import os
    import matplotlib.pyplot as plt
    return mo, pd, pl, os, plt


@app.cell
def _(mo):
    return mo.md("""
### 🔧 Patch Data Analysis Summary

This notebook performs analysis on automatically generated patches.

**Main Columns:**
- `Tool`
- `Category`
- `Patch`
- `GitHub Link`
- `ChangeType`
- `CodeLine`
- `RequireType`

**Main Goals:**
1. Count patches by change type
2. Count patches by tool
3. Show distribution across categories
4. Analyze how `require` is used across bug types
""")



@app.cell
def _(mo, pl):
    inv_df = pl.read_csv(str(mo.notebook_location() / "public" / "patches_w_require.csv"),infer_schema_length=10000)
    return inv_df

@app.cell
def _(inv_df):
    inv_df
    return inv_df

@app.cell
def _(inv_df, pl):
    counts = (
        inv_df
        .group_by("ChangeType")
        .agg(pl.len().alias("Count"))  
    )
    counts
    return counts

@app.cell
def _(inv_df, pl):
    tool_counts = (
        inv_df
        .group_by("Tool")
        .agg(pl.len().alias("PatchCount")) 
        .sort("PatchCount", descending=True)
    )
    tool_counts
    return tool_counts

@app.cell
def _(inv_df, pl):
    tool_change = (
        inv_df
        .group_by(["Tool", "ChangeType"])
        .agg(pl.len().alias("Count"))  
        .pivot(values="Count", index="Tool", on="ChangeType")
        .fill_null(0)
    )
    tool_change
    return tool_change

@app.cell
def _(inv_df, pl):
    category_counts = (
        inv_df
        .group_by("Category")
        .agg(pl.len().alias("Count")) 
        .sort("Count", descending=True)
    )
    category_counts
    return category_counts

@app.cell
def _(inv_df, pl):
    req_cat = (
        inv_df
        .group_by(["RequireType", "Category"])
        .agg(pl.len().alias("Count"))  # and here
        .pivot(values="Count", index="RequireType", on="Category") 
        .fill_null(0)
    )
    req_cat
    return req_cat

if __name__ == "__main__":
    app.run()
