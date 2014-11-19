<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" omit-xml-declaration="yes" indent="no"/>
<xsl:strip-space elements="*"/>

<xsl:variable name="tasks" select="document('sort.xml')/task"/>

<xsl:template match="/">
	<xsl:value-of select="task/cmd"/>
	<xsl:apply-templates select="task/options/option"/>
</xsl:template>

<xsl:template match="option">
	<xsl:value-of select="concat(' ', normalize-space(.), ' ', ./@default)"/>
</xsl:template>

</xsl:stylesheet>