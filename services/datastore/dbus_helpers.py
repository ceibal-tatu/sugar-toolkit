# Copyright (C) 2006, Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


# Mostly taken from dbus-python's service.py

import dbus
from dbus import service
import inspect

def method(dbus_interface, in_signature=None, out_signature=None, async_callbacks=None, sender_keyword=None, dbus_message_keyword=None):
    dbus._util._validate_interface_or_name(dbus_interface)

    def decorator(func):
        args = inspect.getargspec(func)[0]
        args.pop(0)

        if async_callbacks:
            if type(async_callbacks) != tuple:
                raise TypeError('async_callbacks must be a tuple of (keyword for return callback, keyword for error callback)')
            if len(async_callbacks) != 2:
                raise ValueError('async_callbacks must be a tuple of (keyword for return callback, keyword for error callback)')
            args.remove(async_callbacks[0])
            args.remove(async_callbacks[1])

        if sender_keyword:
            args.remove(sender_keyword)

        if dbus_message_keyword:
            args.remove(dbus_message_keyword)

        if in_signature:
            in_sig = tuple(dbus.dbus_bindings.Signature(in_signature))

            if len(in_sig) > len(args):
                raise ValueError, 'input signature is longer than the number of arguments taken'
            elif len(in_sig) < len(args):
                raise ValueError, 'input signature is shorter than the number of arguments taken'

        func._dbus_message_keyword = dbus_message_keyword
        func._dbus_is_method = True
        func._dbus_async_callbacks = async_callbacks
        func._dbus_interface = dbus_interface
        func._dbus_in_signature = in_signature
        func._dbus_out_signature = out_signature
        func._dbus_sender_keyword = sender_keyword
        func._dbus_args = args
        return func

    return decorator

def fallback_signal(dbus_interface, signature=None, ignore_args=None):
    dbus._util._validate_interface_or_name(dbus_interface)
    def decorator(func):
        def emit_signal(self, *args, **keywords):
            obj_path = func(self, *args, **keywords)
            message = dbus.dbus_bindings.Signal(obj_path, dbus_interface, func.__name__)
            iter = message.get_iter(True)

            if emit_signal._dbus_signature:
                signature = tuple(dbus.dbus_bindings.Signature(emit_signal._dbus_signature))
                for (arg, sig) in zip(args, signature):
                    iter.append_strict(arg, sig)
            else:
                for arg in args:
                    iter.append(arg)

            self._connection.send(message)

        temp_args = inspect.getargspec(func)[0]
        temp_args.pop(0)

        args = []
        for arg in temp_args:
            if arg not in ignore_args:
                args.append(arg)

        if signature:
            sig = tuple(dbus.dbus_bindings.Signature(signature))

            if len(sig) > len(args):
                raise ValueError, 'signal signature is longer than the number of arguments provided'
            elif len(sig) < len(args):
                raise ValueError, 'signal signature is shorter than the number of arguments provided'

        emit_signal.__name__ = func.__name__
        emit_signal.__doc__ = func.__doc__
        emit_signal._dbus_is_signal = True
        emit_signal._dbus_interface = dbus_interface
        emit_signal._dbus_signature = signature
        emit_signal._dbus_args = args
        return emit_signal

    return decorator

class FallbackObject(dbus.service.Object):
    """A base class for exporting your own Objects across the Bus.

    Just inherit from Object and provide a list of methods to share
    across the Bus
    """
    def __init__(self, bus_name, fallback_object_path):
        self._object_path = fallback_object_path
        self._name = bus_name 
        self._bus = bus_name.get_bus()
            
        self._connection = self._bus.get_connection()

        self._connection.register_fallback(fallback_object_path, self._unregister_cb, self._message_cb)

    def _message_cb(self, connection, message):
        try:
            # lookup candidate method and parent method
            method_name = message.get_member()
            interface_name = message.get_interface()
            (candidate_method, parent_method) = dbus.service._method_lookup(self, method_name, interface_name)

            # set up method call parameters
            args = message.get_args_list()
            keywords = {}

            # iterate signature into list of complete types
            if parent_method._dbus_out_signature:
                signature = tuple(dbus.dbus_bindings.Signature(parent_method._dbus_out_signature))
            else:
                signature = None

            # set up async callback functions
            if parent_method._dbus_async_callbacks:
                (return_callback, error_callback) = parent_method._dbus_async_callbacks
                keywords[return_callback] = lambda *retval: dbus.service._method_reply_return(connection, message, method_name, signature, *retval)
                keywords[error_callback] = lambda exception: dbus.service._method_reply_error(connection, message, exception)

            # include the sender if desired
            if parent_method._dbus_sender_keyword:
                keywords[parent_method._dbus_sender_keyword] = message.get_sender()

            if parent_method._dbus_message_keyword:
                keywords[parent_method._dbus_message_keyword] = message

            # call method
            retval = candidate_method(self, *args, **keywords)

            # we're done - the method has got callback functions to reply with
            if parent_method._dbus_async_callbacks:
                return

            # otherwise we send the return values in a reply. if we have a
            # signature, use it to turn the return value into a tuple as
            # appropriate
            if parent_method._dbus_out_signature:
                # if we have zero or one return values we want make a tuple
                # for the _method_reply_return function, otherwise we need
                # to check we're passing it a sequence
                if len(signature) == 0:
                    if retval == None:
                        retval = ()
                    else:
                        raise TypeError('%s has an empty output signature but did not return None' %
                            method_name)
                elif len(signature) == 1:
                    retval = (retval,)
                else:
                    if operator.isSequenceType(retval):
                        # multi-value signature, multi-value return... proceed unchanged
                        pass
                    else:
                        raise TypeError('%s has multiple output values in signature %s but did not return a sequence' %
                            (method_name, signature))

            # no signature, so just turn the return into a tuple and send it as normal
            else:
                signature = None
                if retval == None:
                    retval = ()
                else:
                    retval = (retval,)

            dbus.service._method_reply_return(connection, message, method_name, signature, *retval)
        except Exception, exception:
            # send error reply
            dbus.service._method_reply_error(connection, message, exception)

    @method('org.freedesktop.DBus.Introspectable', in_signature='', out_signature='s', dbus_message_keyword="dbus_message")
    def Introspect(self, dbus_message=None):
        reflection_data = '<!DOCTYPE node PUBLIC "-//freedesktop//DTD D-BUS Object Introspection 1.0//EN" "http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd">\n'
        op = dbus_message.get_path()
        reflection_data += '<node name="%s">\n' % (op)

        interfaces = self._dbus_class_table[self.__class__.__module__ + '.' + self.__class__.__name__]
        for (name, funcs) in interfaces.iteritems():
            reflection_data += '  <interface name="%s">\n' % (name)

            for func in funcs.values():
                if getattr(func, '_dbus_is_method', False):
                    reflection_data += self.__class__._reflect_on_method(func)
                elif getattr(func, '_dbus_is_signal', False):
                    reflection_data += self.__class__._reflect_on_signal(func)

            reflection_data += '  </interface>\n'

        reflection_data += '</node>\n'

        return reflection_data

    def __repr__(self):
        return '<dbus_helpers.FallbackObject %s on %r at %#x>' % (self._fallback_object_path, self._name, id(self))
    __str__ = __repr__
