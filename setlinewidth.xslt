<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:svg="http://www.w3.org/2000/svg">

<xsl:param name="default_stroke_width" select="1"/>

<xsl:template match="//svg:polygon[not(@stroke-width)]">
	<xsl:copy>
		<xsl:attribute name="stroke-width"><xsl:value-of select="$default_stroke_width"/></xsl:attribute>
		<xsl:apply-templates select="node()|@*"/>
	</xsl:copy>
</xsl:template>

<xsl:template match="node()|@*">
	<xsl:copy>
		<xsl:apply-templates select="node()|@*"/>
	</xsl:copy>
</xsl:template>

</xsl:stylesheet>
