/* -*- mode: C; c-basic-offset: 4 -*- 
 *
 * PyCairo - Python bindings for Cairo
 *
 * Copyright © 2003-2004 James Henstridge
 *
 * This library is free software; you can redistribute it and/or
 * modify it either under the terms of the GNU Lesser General Public
 * License version 2.1 as published by the Free Software Foundation
 * (the "LGPL") or, at your option, under the terms of the Mozilla
 * Public License Version 1.1 (the "MPL"). If you do not alter this
 * notice, a recipient may use your version of this file under either
 * the MPL or the LGPL.
 *
 * You should have received a copy of the LGPL along with this library
 * in the file COPYING-LGPL-2.1; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 * You should have received a copy of the MPL along with this library
 * in the file COPYING-MPL-1.1
 *
 * The contents of this file are subject to the Mozilla Public License
 * Version 1.1 (the "License"); you may not use this file except in
 * compliance with the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * This software is distributed on an "AS IS" basis, WITHOUT WARRANTY
 * OF ANY KIND, either express or implied. See the LGPL or the MPL for
 * the specific language governing rights and limitations.
 *
 * Contributor(s):
 *
 */

#ifndef _PYCAIRO_PRIVATE_H_
#define _PYCAIRO_PRIVATE_H_

#ifdef _PYCAIRO_H_
#  error "don't include pycairo.h and pycairo-private.h together"
#endif

#define _INSIDE_PYCAIRO_
#include "pycairo.h"


extern PyTypeObject PyCairoMatrix_Type;
extern PyTypeObject PyCairoContext_Type;
extern PyTypeObject PyCairoSurface_Type;
extern PyTypeObject PyCairoPattern_Type;
extern PyTypeObject PyCairoFont_Type;

int       pycairo_check_status(cairo_status_t status);

/* takes ownership of reference */
PyObject *pycairo_matrix_wrap(cairo_matrix_t *matrix);
PyObject *pycairo_context_wrap(cairo_t *ctx);
PyObject *pycairo_surface_wrap(cairo_surface_t *surface);
PyObject *pycairo_pattern_wrap(cairo_pattern_t *pattern);
PyObject *pycairo_font_wrap(cairo_font_t *font);

#endif /* _PYCAIRO_PRIVATE_H_ */
