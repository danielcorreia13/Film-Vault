<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="movie">
        <h1><xsl:value-of select="original-title"/></h1>
        <img class="img_film">
            <xsl:attribute name="src">
                <xsl:value-of select="cover-url"/>
            </xsl:attribute>
        </img>
        <div class="rating">
            <h5>Rating: <xsl:value-of select="rating"/>/10</h5>
            <h6>Number of votes: <xsl:value-of select="votes"/> </h6>
        </div>

            <xsl:variable name="count" select="11"/>
            <table>
                <tr>
                    <th>Actor</th>
                    <th>Characters</th>
                </tr>
                <xsl:for-each select="cast/person">
                    <xsl:if test="position() &lt; $count">
                    <tr>
                        <td><xsl:value-of select="name"/></td>
                        <td><xsl:value-of select="current-role/character/name"/></td>
                    </tr>
                    </xsl:if>
                </xsl:for-each>
            </table>

        <h4>Directors: <xsl:for-each select="directors"> <xsl:value-of select="person/name" separator=","/></xsl:for-each> </h4>
        <h4>Writers: <xsl:for-each select="writers"> <xsl:value-of select="person/name" separator=","/></xsl:for-each> </h4>
        <h5>Runtime : <xsl:value-of select="runtimes/item"/> min</h5>
        <h5>Genres: <xsl:for-each select="genres"> <xsl:value-of select="item" separator=","/></xsl:for-each></h5>
        <h5>Original Air Date: <xsl:value-of select="original-air-date"/></h5>
        <h6>Languages: <xsl:value-of select="languages" /></h6>
        <h6>Plot: <xsl:value-of select="plot-outline"/></h6>
        <h7>Synopsis: <xsl:value-of select="synopsis/item"/></h7>

    </xsl:template>

</xsl:stylesheet>