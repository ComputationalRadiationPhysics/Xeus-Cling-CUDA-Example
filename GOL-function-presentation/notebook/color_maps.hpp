#ifndef COLOR_MAPS_H
#define COLOR_MAPS_H

template <typename varTyp>
struct ColorMap
{
	virtual int r(varTyp value){return (2500 + 500 * value)%65535;}
	virtual int g(varTyp value){return (10408 + 500 * value)%65535;}
	virtual int b(varTyp value){return (7401 + 500 * value)%65535;}
};

template <typename varTyp>
struct BlackWhiteMap : ColorMap<varTyp>
{
	int r(varTyp value){return value ? 65535 : 0;}
	int g(varTyp value){return value ? 65535 : 0;}
	int b(varTyp value){return value ? 65535 : 0;}
};

#endif