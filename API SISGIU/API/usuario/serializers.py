from rest_framework import serializers
from usuario.models import (
    Usuario,
    Estudiante,
    TipoPostgrado,
    EstadoEstudiante,
    PersonalDocente,
    PersonalAdministrativo,
    )
from usuario.utils import send_welcome_mail


"""
Serializer de Usuario/Administrador
"""


class AdministradorListSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = Usuario
        fields = ('id', 'is_staff', 'is_superuser', 'tipo_documento', 'cedula', 'first_name', 'segundo_nombre',
                  'last_name', 'segundo_apellido', 'last_name', 'email',
                  'correo_alternativo', 'celular', 'telefono_casa', 'telefono_trabajo',
                  'fecha_nacimiento', 'sexo', 'nacionalidad', 'estado_civil', 'foto', 'username', 'password')

    def create(self, validated_data):
        user_data = validated_data
        try:
            user = Usuario.objects.get(cedula=user_data['cedula'])
            user.is_superuser = True;
            user.is_staff = True;
            user.save()
            send_welcome_mail("Administrador", user.__dict__)
            return user
        except Exception as e:
            password = validated_data.pop('password', None)
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
            instance.save()
            send_welcome_mail("Administrador", validated_data)
            return instance


# Todo menos el username (no se debe "re-poner")
class AdministradorDetailSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = Usuario
        fields = ('tipo_documento', 'cedula', 'is_staff', 'is_superuser', 'first_name', 'segundo_nombre',
                  'last_name', 'segundo_apellido', 'last_name', 'email',
                  'correo_alternativo', 'celular', 'telefono_casa', 'telefono_trabajo',
                  'fecha_nacimiento', 'sexo', 'nacionalidad', 'estado_civil', 'foto', 'username', 'password')

    def update(self, instance, validated_data):
        usuario = validated_data

        admin_usuario = Usuario.objects.get(cedula=usuario['cedula'])
        admin_usuario.first_name = usuario['first_name']
        if(admin_usuario.password != usuario['password']):
            admin_usuario.set_password(usuario['password'])
        admin_usuario.segundo_nombre = usuario['segundo_nombre']
        admin_usuario.last_name = usuario['last_name']
        admin_usuario.segundo_apellido = usuario['segundo_apellido']
        admin_usuario.email = usuario['email']
        admin_usuario.correo_alternativo = usuario['correo_alternativo']
        admin_usuario.celular = usuario['celular']
        admin_usuario.telefono_casa = usuario['telefono_casa']
        admin_usuario.telefono_trabajo = usuario['telefono_trabajo']
        admin_usuario.fecha_nacimiento = usuario['fecha_nacimiento']
        admin_usuario.sexo = usuario['sexo']
        admin_usuario.nacionalidad = usuario['nacionalidad']
        admin_usuario.estado_civil = usuario['estado_civil']
        if(usuario.get('foto')):
            admin_usuario.foto = usuario['foto']

        admin_usuario.save()

        return instance

"""
Serializer de Usuario Generico
"""


class UsuarioListSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = Usuario
        fields = ('id', 'tipo_documento', 'cedula', 'first_name', 'segundo_nombre',
                  'last_name', 'segundo_apellido', 'last_name', 'email',
                  'correo_alternativo', 'celular', 'telefono_casa', 'telefono_trabajo',
                  'fecha_nacimiento', 'sexo', 'nacionalidad', 'estado_civil', 'foto', 'username', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UsuarioDetailSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = Usuario
        fields = ('tipo_documento', 'cedula', 'first_name', 'segundo_nombre',
                  'last_name', 'segundo_apellido', 'last_name', 'email',
                  'correo_alternativo', 'celular', 'telefono_casa', 'telefono_trabajo',
                  'fecha_nacimiento', 'sexo', 'nacionalidad', 'estado_civil', 'foto', 'password')

"""
Serializer de TipoPostgrado
"""


class TipoPostgradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPostgrado
        fields = ('__all__')

"""
Serializer de EstadoEstudiante
"""


class EstadoEstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoEstudiante
        fields = ('__all__')

"""
Serializer de Estudiante
"""


class EstudianteSerializer(serializers.ModelSerializer):
    usuario = UsuarioListSerializer()

    class Meta:
        model = Estudiante
        fields = ('usuario', 'id_tipo_postgrado', 'id_estado_estudiante', 'direccion',)

    def create(self, validated_data):
        print("############################")
        user_data = validated_data.pop('usuario')
        try:
            estudiante = Estudiante.objects.get(usuario__cedula=user_data['cedula'])
            return estudiante
        except:
            try:
                user = Usuario.objects.get(cedula=user_data['cedula'])
                estudiante, created = Estudiante.objects.update_or_create(
                                    usuario=user,
                                    id_tipo_postgrado=validated_data.pop('id_tipo_postgrado'),
                                    id_estado_estudiante=validated_data.pop('id_estado_estudiante'),
                                    direccion=validated_data.pop('direccion')
                                    )
                send_welcome_mail("Estudiante", user)
                return estudiante
            except:
                user = UsuarioListSerializer.create(UsuarioListSerializer(), validated_data=user_data)
                estudiante, created = Estudiante.objects.update_or_create(
                                    usuario=user,
                                    id_tipo_postgrado=validated_data.pop('id_tipo_postgrado'),
                                    id_estado_estudiante=validated_data.pop('id_estado_estudiante'),
                                    direccion=validated_data.pop('direccion')
                                    )
                send_welcome_mail("Estudiante", user)
                return estudiante


class EstudianteDetailSerializer(serializers.ModelSerializer):
    usuario = UsuarioDetailSerializer()

    class Meta:
        model = Estudiante
        fields = ('usuario', 'id_tipo_postgrado', 'id_estado_estudiante', 'direccion',)

    def update(self, instance, validated_data):
        instance.id_tipo_postgrado = validated_data.get('id_tipo_postgrado', instance.id_tipo_postgrado)
        instance.id_estado_estudiante = validated_data.get('id_estado_estudiante',
                                                           instance.id_estado_estudiante)
        instance.direccion = validated_data.get('direccion', instance.direccion)
        instance.save()

        usuario = validated_data.get('usuario')

        estudiante_usuario = Usuario.objects.get(cedula=usuario['cedula'])
        estudiante_usuario.first_name = usuario['first_name']
        if(estudiante_usuario.password != usuario['password']):
            estudiante_usuario.set_password(usuario['password'])
        estudiante_usuario.segundo_nombre = usuario['segundo_nombre']
        estudiante_usuario.last_name = usuario['last_name']
        estudiante_usuario.segundo_apellido = usuario['segundo_apellido']
        estudiante_usuario.email = usuario['email']
        estudiante_usuario.correo_alternativo = usuario['correo_alternativo']
        estudiante_usuario.celular = usuario['celular']
        estudiante_usuario.telefono_casa = usuario['telefono_casa']
        estudiante_usuario.telefono_trabajo = usuario['telefono_trabajo']
        estudiante_usuario.fecha_nacimiento = usuario['fecha_nacimiento']
        estudiante_usuario.sexo = usuario['sexo']
        estudiante_usuario.nacionalidad = usuario['nacionalidad']
        estudiante_usuario.estado_civil = usuario['estado_civil']
        if(usuario.get('foto')):
            estudiante_usuario.foto = usuario['foto']

        estudiante_usuario.save()

        return instance

"""
Serializer de Docente
"""


class DocenteSerializer(serializers.ModelSerializer):
    usuario = UsuarioListSerializer()
    curriculum = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    rif = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    permiso_ingresos = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta:
        model = PersonalDocente
        fields = ('usuario', 'curriculum', 'rif', 'direccion', 'permiso_ingresos', 'coordinador', 'id_tipo_postgrado')

    def create(self, validated_data):
        user_data = validated_data.pop('usuario')
        try:
            docente = PersonalDocente.objects.get(usuario__cedula=user_data['cedula'])
            return docente
        except:
            try:
                user = Usuario.objects.get(cedula=user_data['cedula'])
                docente, created = PersonalDocente.objects.update_or_create(
                    usuario=user,
                    curriculum=validated_data.get('curriculum'),
                    rif=validated_data.get('rif'),
                    direccion=validated_data.pop('direccion'),
                    permiso_ingresos=validated_data.get('permiso_ingresos'),
                    coordinador=validated_data.pop('coordinador'),
                    id_tipo_postgrado=validated_data.pop('id_tipo_postgrado'))
                send_welcome_mail("Docente", user)
                return docente
            except:
                user = UsuarioListSerializer.create(UsuarioListSerializer(), validated_data=user_data)
                docente, created = PersonalDocente.objects.update_or_create(
                                    usuario=user,
                                    curriculum=validated_data.get('curriculum'),
                                    rif=validated_data.get('rif'),
                                    direccion=validated_data.pop('direccion'),
                                    permiso_ingresos=validated_data.get('permiso_ingresos'),
                                    coordinador=validated_data.pop('coordinador'),
                                    id_tipo_postgrado=validated_data.pop('id_tipo_postgrado'))
                send_welcome_mail("Docente", user)
                return docente


class DocenteDetailSerializer(serializers.ModelSerializer):
    usuario = UsuarioDetailSerializer()
    curriculum = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    rif = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    permiso_ingresos = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)

    class Meta:

        model = PersonalDocente
        fields = ('usuario', 'curriculum', 'rif', 'direccion', 'permiso_ingresos', 'coordinador', 'id_tipo_postgrado')

    def update(self, instance, validated_data):

        if(instance.curriculum is not None):
            instance.curriculum = validated_data.get('curriculum', instance.curriculum)

        if(instance.rif is not None):
            instance.rif = validated_data.get('rif', instance.rif)

        if(instance.permiso_ingresos is not None):
            instance.permiso_ingresos = validated_data.get('permiso_ingresos', instance.permiso_ingresos)

        instance.coordinador = validated_data.get('coordinador', instance.coordinador)
        instance.id_tipo_postgrado = validated_data.get('id_tipo_postgrado', instance.id_tipo_postgrado)
        instance.direccion = validated_data.get('direccion', instance.direccion)
        instance.save()

        usuario = validated_data.get('usuario')

        docente_usuario = Usuario.objects.get(cedula=usuario['cedula'])
        if(docente_usuario.password != usuario['password']):
            docente_usuario.set_password(usuario['password'])
        docente_usuario.first_name = usuario['first_name']
        docente_usuario.segundo_nombre = usuario['segundo_nombre']
        docente_usuario.last_name = usuario['last_name']
        docente_usuario.segundo_apellido = usuario['segundo_apellido']
        docente_usuario.email = usuario['email']
        docente_usuario.correo_alternativo = usuario['correo_alternativo']
        docente_usuario.celular = usuario['celular']
        docente_usuario.telefono_casa = usuario['telefono_casa']
        docente_usuario.telefono_trabajo = usuario['telefono_trabajo']
        docente_usuario.fecha_nacimiento = usuario['fecha_nacimiento']
        docente_usuario.sexo = usuario['sexo']
        docente_usuario.nacionalidad = usuario['nacionalidad']
        docente_usuario.estado_civil = usuario['estado_civil']

        if(usuario.get('foto')):
            docente_usuario.foto = usuario['foto']

        docente_usuario.save()

        return instance


"""
Serializer de PersonalAdministrativo
"""


class AdministrativoSerializer(serializers.ModelSerializer):
    usuario = UsuarioListSerializer()

    class Meta:
        model = PersonalAdministrativo
        fields = ('__all__')

    def create(self, validated_data):
        user_data = validated_data.pop('usuario')
        try:
            personal_admin = PersonalAdministrativo.objects.get(usuario__cedula=user_data['cedula'])
            return personal_admin
        except:
            try:
                user = Usuario.objects.get(cedula=user_data['cedula'])
                personal_admin, created = PersonalAdministrativo.objects.update_or_create(usuario=user)
                send_welcome_mail("Administrativo", user)
                return personal_admin
            except:
                user = UsuarioListSerializer.create(UsuarioListSerializer(), validated_data=user_data)
                personal_admin, created = PersonalAdministrativo.objects.update_or_create(usuario=user)
                send_welcome_mail("Administrativo", user)
                return personal_admin


class AdministrativoDetailSerializer(serializers.ModelSerializer):
    usuario = UsuarioDetailSerializer()

    class Meta:
        model = PersonalAdministrativo
        fields = ('__all__')

    def update(self, instance, validated_data):
        usuario = validated_data.get('usuario')
        administrativo_usuario = Usuario.objects.get(cedula=usuario['cedula'])

        if(administrativo_usuario.password != usuario['password']):
            administrativo_usuario.set_password(usuario['password'])
        administrativo_usuario.first_name = usuario['first_name']
        administrativo_usuario.segundo_nombre = usuario['segundo_nombre']
        administrativo_usuario.last_name = usuario['last_name']
        administrativo_usuario.segundo_apellido = usuario['segundo_apellido']
        administrativo_usuario.email = usuario['email']
        administrativo_usuario.correo_alternativo = usuario['correo_alternativo']
        administrativo_usuario.celular = usuario['celular']
        administrativo_usuario.telefono_casa = usuario['telefono_casa']
        administrativo_usuario.telefono_trabajo = usuario['telefono_trabajo']
        administrativo_usuario.fecha_nacimiento = usuario['fecha_nacimiento']
        administrativo_usuario.sexo = usuario['sexo']
        administrativo_usuario.nacionalidad = usuario['nacionalidad']
        administrativo_usuario.estado_civil = usuario['estado_civil']
        if(usuario.get('foto')):
            administrativo_usuario.foto = usuario['foto']

        administrativo_usuario.save()

        personal_admin, created = PersonalAdministrativo.objects.update_or_create(
                                usuario=administrativo_usuario)
        return personal_admin
