from mcp.server.fastmcp import FastMCP

mcp = FastMCP("maritime-clinical-context")

@mcp.tool()
def normal_vital_ranges() -> dict:
    return {"breathing_rate":"12-16/min","oxygen_saturation":"95-100%","pulse":"60-80/min","blood_pressure":"120-140/60-90","capillary_response":"<2 sec","blood_sugar":"4-7 mmol/liter"}


@mcp.tool()
def oxygen_delivery_guidance(flow_l_min: float) -> str:
    if flow_l_min <= 5:
        return "Nasal cannula may be suitable up to 5 l/min."
    if flow_l_min > 10:
        return "Use Hudson mask for oxygen above 10 l/min unless another method is clinically justified."
    return "Document delivery method and reassess oxygen saturation."

if __name__ == "__main__":
    mcp.run()
