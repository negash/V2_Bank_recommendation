def format_final_response(customer_name, result):
    """Format the final recommendation response.Also, emoji add to make it look nice in the output file"""
    output = f"✨ Recommendation for {customer_name}\n\n"

    labels = ["Safe", "Balanced", "Growth"]

    for i, rec in enumerate(result["recommendations"], 1):
        label = labels[i - 1] if i - 1 < len(labels) else f"Option {i}"

        output += f"""🔹 Option {i} — {label} 
        
 Recommendation:
{rec['action']}

 Reason:
{rec['reason']}

 Risk Level:
{rec['risk_level'].capitalize()}

 Confidence:
{rec['confidence']:.2f}

"""

    return output
