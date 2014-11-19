<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" omit-xml-declaration="yes" indent="no"/>
<xsl:strip-space elements="*"/>

<xsl:variable name="tasks" select="document('sort.xml')"/>

<xsl:template match="pipeline">
	<xsl:for-each select="./step">
		<xsl:call-template name="task">
			<xsl:with-param name="stepContent" select="$tasks/task[@name='sort']"/>
			<xsl:with-param name="params" select="./*"/>
		</xsl:call-template>
	</xsl:for-each>
</xsl:template>

<xsl:template name="task">
	<xsl:param name="stepContent"/>
	<xsl:param name="params"/>
	<xsl:value-of select="$stepContent/cmd"/>
	<xsl:apply-templates select="$stepContent/options/option">
			<xsl:with-param name="actualParams" select="$params"/>
	</xsl:apply-templates>
</xsl:template>

<xsl:template match="option">
	<xsl:param name="actualParams"/>
	<xsl:variable name="optionName" select="./@name"/>
	<xsl:choose>
		<xsl:when test="$actualParams/*[name()=$optionName]">
			<xsl:value-of select="concat(' ', normalize-space(.), ' ')"/>
			<xsl:value-of select="$actualParams/*[name()=$optionName]"/>
		</xsl:when>
		<xsl:otherwise>
			<xsl:if test="./@default">
				<xsl:value-of select="concat(' ', normalize-space(.), ' ')"/>
				<xsl:value-of select="./@default"/>
			</xsl:if>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>


</xsl:stylesheet>