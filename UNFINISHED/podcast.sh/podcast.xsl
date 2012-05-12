<xsl:stylesheet version = '1.0' xmlns:xsl='http://www.w3.org/1999/XSL/Transform' xmlns:xspf="http://xspf.org/ns/0/">
<xsl:output method="text"/>
<xsl:template match="/">	
<xsl:text>#EXTM3U
</xsl:text>
<xsl:for-each select="//trackList/track">
#EXTINF:-1,<xsl:value-of select="creator"/> - <xsl:value-of select="title"/>
<xsl:text>
</xsl:text>
<xsl:value-of select="location"/>
<xsl:text>
</xsl:text>
</xsl:for-each> 
</xsl:template>
</xsl:stylesheet>
